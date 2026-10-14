import com.ddd.services.smartconversation.context.distress_fall.ContextDistressFallDetected;
import com.google.gson.JsonObject;
import java.nio.file.*;
/**
 * KS-831: renders the production fall prompt from the real Java, with @@HISTORY@@ as the history
 * slot and the additionalInformation keys production sends (seniorName, seniorGender, currentTime).
 *
 * Compile against grandappflutter's DddSmartConversation sources (AssistantResponse, ConversationOutcome,
 * context/*) and gson, then:  java RenderLab data/prompts/prompt_ks831_new.txt Jake
 */
public class RenderLab {
  public static void main(String[] a) throws Exception {
    JsonObject info = new JsonObject();
    info.addProperty("seniorName", a[1]);
    info.addProperty("seniorGender", "male");
    info.addProperty("currentTime", "2026-10-06T18:39:45.000");
    String p = new ContextDistressFallDetected("en", "female", info).buildPrompt(new String[]{"@@HISTORY@@"});
    Files.write(Paths.get(a[0]), p.getBytes("UTF-8"));
  }
}
