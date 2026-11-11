
import pandas as pd

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. Dataset
iris = load_iris()

X = iris.data
y = iris.target

# 2. Train və test məlumatları
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# 3. Model yarat
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# 4. Modeli öyrət
model.fit(X_train, y_train)

print("AI modeli öyrədildi!")

# 5. Modeli test et
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Modelin dəqiqliyi:", accuracy * 100, "%")

# 6. Yeni məlumat daxil et
print("\n--- AI Flower Classifier ---")

sepal_length = float(input("Sepal Length: "))
sepal_width = float(input("Sepal Width: "))
petal_length = float(input("Petal Length: "))
petal_width = float(input("Petal Width: "))

new_flower = [[
    sepal_length,
    sepal_width,
    petal_length,
    petal_width
]]

# 7. Proqnoz
result = model.predict(new_flower)

flower_name = iris.target_names[result[0]]

print("\nAI nəticəsi:", flower_name)
