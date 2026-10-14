import com.ddd.services.smartconversation.context.ContextBase;
import com.ddd.services.smartconversation.context.ContextFactory;
import com.ddd.services.smartconversation.context.ContextType;
import com.google.gson.JsonObject;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * KS-831: renders every conversation prompt (each ContextType x en-US / he-IL / pt-PT) from the real
 * Java, with @@HISTORY@@ as the history slot and the additionalInformation keys production sends for
 * a fall call (seniorName, seniorGender, currentTime).
 *
 * Driven by render_ks831.py, which compiles it against the DddSmartConversation sources of a git ref.
 * Usage: java RenderAll <outDir> <englishSeniorName>
 */
public class RenderAll {
	public static void main(String[] a) throws Exception {
		Path out = Paths.get(a[0]);
		Files.createDirectories(out);
		for (ContextType type : ContextType.values()) {
			for (String language : new String[] { "en-US", "he-IL", "pt-PT" }) {
				JsonObject info = new JsonObject();
				// English keeps the earlier labs' name; Hebrew and Portuguese get a local one (KS-833 used Manuel).
				info.addProperty("seniorName", language.startsWith("he") ? "David" : language.startsWith("pt") ? "Manuel" : a[1]);
				info.addProperty("seniorGender", "male");
				info.addProperty("currentTime", "2026-10-06T18:39:45.000");
				if (type != ContextType.DISTRESS_FALL_DETECTED) {
					// The keys LanguagePromptPinTest uses; the fall prompt keeps production's three.
					info.addProperty("scheduledTime", "08:00");
					info.addProperty("medicationName", "Aspirin");
				}
				String prompt;
				try {
					ContextBase context = ContextFactory.fromContextType(type, language, "female", info);
					if (context == null) {
						continue;
					}
					prompt = context.buildPrompt(new String[] { "@@HISTORY@@" });
				} catch (RuntimeException e) {
					// Some medication contexts need inputs a fall call never has; they are only
					// rendered to prove KS-831 leaves them alone, so a skip is reported, not fatal.
					System.err.println("skipped " + type + " " + language + ": " + e);
					continue;
				}
				Files.write(out.resolve(type.name() + "_" + language + ".txt"), prompt.getBytes(StandardCharsets.UTF_8));
			}
		}
	}
}
