import requests

from flask import Flask, render_template, request, jsonify
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

app = Flask(__name__)

# Dataset
iris = load_iris()
X = iris.data
y = iris.target

# Train və test
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# AI model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# Test nəticələri
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)
matrix = confusion_matrix(
    y_test,
    predictions,
    labels=[0, 1, 2]
)

# HTML səhifəsi
@app.route("/")
def home():
    return render_template("index.html")


# Dashboard məlumatları
@app.route("/api/dashboard")
def dashboard():

    flowers = []

    for i in range(len(X)):
        flowers.append({
            "petal_length": float(X[i][2]),
            "petal_width": float(X[i][3]),
            "class": iris.target_names[y[i]]
        })

    return jsonify({
        "accuracy": round(accuracy * 100, 2),
        "classes": iris.target_names.tolist(),
        "matrix": matrix.tolist(),
        "flowers": flowers
    })


def search_flower_image(flower_name):

    search_queries = {
        "setosa": "Iris setosa flower",
        "versicolor": "Iris versicolor flower",
        "virginica": "Iris virginica flower"
    }

    query = search_queries.get(flower_name)

    if not query:
        return None

    url = "https://commons.wikimedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": 6,
        "gsrlimit": 5,
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": 600
    }

    headers = {
        "User-Agent": "AIFlowerClassifier/1.0"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        pages = data.get("query", {}).get("pages", {})

        for page in pages.values():

            image_info = page.get("imageinfo", [])

            if image_info:
                info = image_info[0]

                image_url = info.get("thumburl") or info.get("url")

                if image_url:
                    return {
                        "image_url": image_url,
                        "title": page.get("title"),
                        "source_url": info.get("descriptionurl")
                    }

    except requests.RequestException as error:
        print("Image search error:", error)

    return None



# Yeni gülün proqnozu

@app.route("/api/predict", methods=["POST"])
def predict():

    data = request.get_json()

    values = [[
        float(data["sepal_length"]),
        float(data["sepal_width"]),
        float(data["petal_length"]),
        float(data["petal_width"])
    ]]

    prediction = model.predict(values)[0]

    probabilities = model.predict_proba(values)[0]

    flower_name = str(iris.target_names[prediction])

    # İnternetdən şəkil axtarırıq
    image = search_flower_image(flower_name)

    return jsonify({
        "flower": flower_name,
        "confidence": round(
            float(probabilities[prediction]) * 100, 2
        ),
        "image": image
    })


if __name__ == "__main__":
    app.run(debug=True)
