from src import initialize_app

app = initialize_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)