import com.ddd.services.smartconversation.AssistantResponse;
import com.ddd.services.smartconversation.ConversationOutcome;
import com.ddd.services.smartconversation.context.ContextBase;
import com.ddd.services.smartconversation.context.ContextFactory;
import com.ddd.services.smartconversation.context.ContextType;
import com.ddd.services.smartconversation.context.language.FallPromptFamily;
import com.google.gson.JsonObject;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * KS-881: renders the fall prompt from the real Java for en-US / he-IL / pt-PT, twice: for a named
 * senior (the keys production sends: seniorName, seniorGender, currentTime) and for a call where
 * nobody is identified (multiplePeoplePresent, NUN-1592), with @@HISTORY@@ as the history slot.
 *
 * Also writes SERVER_CHECKS.json: what the server's own checks (ContextDistressFallDetected.enforceTurnLimit)
 * do per language, read from the real method: the senior turn on which an open call is stopped, and the
 * closing it speaks when the senior spoke / never spoke (KS-881 lab, 2026-11-03).
 *
 * Driven by render_ks881.py. Usage: java RenderKs881 <outDir>
 */
public class RenderKs881 {
	public static void main(String[] a) throws Exception {
		Path out = Paths.get(a[0]);
		// KS-881: optional second argument COMPACT renders the gpt-6.1-terra prompt family.
		FallPromptFamily family = a.length > 1 ? FallPromptFamily.valueOf(a[1]) : FallPromptFamily.FULL;
		Files.createDirectories(out);
		JsonObject checks = new JsonObject();
		for (String language : new String[] { "en-US", "he-IL", "pt-PT" }) {
			for (boolean unknown : new boolean[] { false, true }) {
				JsonObject info = new JsonObject();
				if (unknown) {
					info.addProperty("multiplePeoplePresent", true);
				} else {
					// The names the KS-831 lab used, so prompts stay comparable.
					info.addProperty("seniorName", language.startsWith("he") ? "David" : language.startsWith("pt") ? "Manuel" : "Jake");
					info.addProperty("seniorGender", "male");
				}
				info.addProperty("currentTime", "2026-10-06T18:39:45.000");
				ContextBase context = ContextFactory.fromContextType(ContextType.DISTRESS_FALL_DETECTED, language, "female", info, family);
				// KS-881 caching: the two parts the server sends (instructions, then input), split by @@SPLIT@@.
				String[] parts = context.buildPromptParts(new String[] { "@@HISTORY@@" });
				String prompt = parts[0] + "\n@@SPLIT@@\n" + parts[1];
				String name = "DISTRESS_FALL_DETECTED_" + language + (unknown ? "_unknown" : "") + ".txt";
				Files.write(out.resolve(name), prompt.getBytes(StandardCharsets.UTF_8));
				if (!unknown) {
					checks.add(language, serverChecks(context));
				}
			}
		}
		Files.write(out.resolve("SERVER_CHECKS.json"), checks.toString().getBytes(StandardCharsets.UTF_8));
	}

	private static JsonObject serverChecks(ContextBase context) {
		AssistantResponse open = new AssistantResponse("...", ConversationOutcome.CONVERSATION_IN_PROGRESS);
		JsonObject j = new JsonObject();
		for (int turns = 1; turns <= 20; turns++) {
			AssistantResponse spoke = context.enforceTurnLimit(history(turns, "hold on"), open);
			if (spoke != open) {
				AssistantResponse silent = context.enforceTurnLimit(history(turns, ContextBase.NO_RESPONSE_MARKER), open);
				j.addProperty("hardStopSeniorTurns", turns);
				j.addProperty("closingSpoke", spoke.getResponseText());
				j.addProperty("outcomeSpoke", spoke.getConversationOutcome().getValue());
				j.addProperty("closingSilent", silent.getResponseText());
				j.addProperty("outcomeSilent", silent.getConversationOutcome().getValue());
				break;
			}
		}
		AssistantResponse noResponse = new AssistantResponse("...", ConversationOutcome.NO_RESPONSE_FROM_RESIDENT);
		AssistantResponse overridden = context.enforceTurnLimit(history(2, "hold on"), noResponse);
		j.addProperty("noResponseAfterSpeechBecomes", overridden.getConversationOutcome().getValue());
		j.addProperty("noResponseAfterSpeechClosing", overridden.getResponseText());
		return j;
	}

	private static String[] history(int turns, String seniorSays) {
		java.util.List<String> lines = new java.util.ArrayList<>();
		lines.add(ContextBase.ASSISTANT_PREFIX + "Hi, it's Vega. Are you okay?");
		for (int i = 0; i < turns; i++) {
			lines.add(ContextBase.USER_PREFIX + seniorSays);
			if (i < turns - 1) {
				lines.add(ContextBase.ASSISTANT_PREFIX + "Are you okay?");
			}
		}
		return lines.toArray(new String[0]);
	}
}
