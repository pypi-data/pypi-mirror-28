from offcrawler.application import app
from modules.repository import repositories

if __name__ == '__main__':
    repositories.connect(host="databasehost", port=3066)
    app.run(debug=True, port=9604, host="0.0.0.0")
