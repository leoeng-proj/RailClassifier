package ui;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Pos;
import javafx.scene.control.Button;
import javafx.scene.control.CheckBox;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.Pane;
import javafx.stage.DirectoryChooser;
import javafx.stage.Stage;

public class UI {
	private static GridPane gp = new GridPane();
	
	public static void initGridPane() {
		gp.setAlignment(Pos.CENTER);
		gp.setVgap(5);
		gp.setHgap(5);
	}
	public static Pane homepage() throws IOException{
		initGridPane();
		TextArea feedback = new TextArea("Feedback From Model");
		feedback.setEditable(false);
		feedback.getStyleClass().add("large-textfield-style");
		gp.add(feedback, 1, 3);
		TextField source = addTextField("Input a Directory For Source", 1, 0);
		TextField result = addTextField("Input a Directory For Results", 1, 1);
		Button browseSource = addButton("Browse", 0, 0, e -> {
			source.setText(showDirectory());			
		});
		Button browseResult = addButton("Browse", 0, 1, e -> {
			result.setText(showDirectory());		
		});
		CheckBox box = new CheckBox("Use Source Directory For Results");
		result.disableProperty().bind(box.selectedProperty());
		browseResult.disableProperty().bind(box.selectedProperty());
		box.setSelected(true);
		gp.add(box, 1, 2);	
		Button classify = addButton("Classify", 2, 0, e -> {
			runClassifier(source.getText(), result.getText(), feedback);			
		});
//		source.setText("C:\\Users\\apoll\\Desktop\\pxfclassify\\Demo\\data");
//		source.setText("C:\\2024-25\\cse248\\final-project\\python\\execTEST\\test");
		classify.disableProperty().bind(source.lengthProperty().isEqualTo(0).or(result.lengthProperty().isEqualTo(0).and(box.selectedProperty().not())));
		return gp;			
	}
	public static void runClassifier(String source, String result, TextArea feedback) {
		if(!confirmInput(source, feedback)) {
			return;
		}
        String scriptPath = "classify.exe";
//      String scriptPath = "C:\\2024-25\\cse248\\final-project\\python\\execTEST\\classify.py";d 
        ProcessBuilder pb = new ProcessBuilder(scriptPath, source, result);
//        pb.directory(new File("RailClassifier"));
//      pb.directory(new File("C:\\2024-25\\cse248\\final-project\\python"));
        pb.redirectErrorStream(true);
        try {
            Process process = pb.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            feedback.clear();
            while ((line = reader.readLine()) != null) {
                feedback.appendText(line+"\n");;
            }
            int exitCode = process.waitFor();
            parseExitCode(exitCode, feedback);
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
	}
	public static boolean confirmInput(String source, TextArea feedback) {
		File test = new File(source);
		boolean b = test.isDirectory();
		if(!b) {
			feedback.setText("Invalid Source\n");
			return b;
		}
		b = test.listFiles().length > 0;
		if(!b) {
			feedback.setText("No Files In Source\n");
			return b;
		}
		return b;
	}
	public static void parseExitCode(int exitCode, TextArea feedback) {
		/*
         * 0	- finished well
         * 200	- no files in input dir
         * 300	- model.p is missing
         */
		String lastFeedback = "";
		switch(exitCode) {
		case 0:
			lastFeedback = "Success!\n";
			break;
		case 200:
			lastFeedback = "No Valid Files In Source\n";
			break;
		case 300:
			lastFeedback = "'model.p' Is Missing\n";
		}
		feedback.appendText(lastFeedback);
	}
	public static String showDirectory() {
		DirectoryChooser directoryChooser = new DirectoryChooser();
		directoryChooser.setTitle("Select Folder");
		File selectedDirectory = directoryChooser.showDialog(new Stage());
		if (selectedDirectory != null) {
		    return selectedDirectory.getAbsolutePath();
		}
		return null;
	}
	public static Button addButton(String name, int x, int y, EventHandler<ActionEvent> e) {
		Button b = new Button(name);
		b.getStyleClass().add("button-style");
		gp.add(b, x, y);
		b.setOnAction(e);
		return b;
	}
	public static TextField addTextField(String text, int x, int y) {
		TextField tf = new TextField();
		tf.setPromptText(text);
		tf.getStyleClass().add("textfield-style");
		gp.add(tf, x, y);
		return tf;
	}
}
