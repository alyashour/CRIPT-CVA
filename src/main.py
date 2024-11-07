from gui.main_window import MainWindow  # Import the MainWindow class from the gui module


def main():
    """Start the application."""
    # Create an instance of the MainWindow
    app = MainWindow()

    # Start the Tkinter main loop to display the window
    app.mainloop()


if __name__ == "__main__":
    main()
