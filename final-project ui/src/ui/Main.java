package ui;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.layout.Pane;
import javafx.stage.Stage;

public class Main extends Application {

	public void start(Stage arg0) throws Exception {
		Pane pane = UI.homepage();
		Scene scene = new Scene(pane);
		scene.getStylesheets().add(getClass().getResource("/resources/styles.css").toExternalForm());
		Stage stage = new Stage();
		stage.setScene(scene);
		stage.setResizable(false);
		stage.setTitle("RailClassifier");
		stage.setHeight(400);
		stage.setWidth(600);
		stage.show();
	}
	public static void main(String[] args) {
		Application.launch(args);
	}	
}
