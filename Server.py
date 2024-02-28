standards = {
    "Tomatoes": {"pH": (6.0, 6.8), "Nitrogen": (50, 200), "Phosphorus": (50, 150), "Potassium": (200, 400), "Organic Carbon": (1, 2)},
    "Wheat": {"pH": (6.0, 7.5), "Nitrogen": (50, 150), "Phosphorus": (25, 75), "Potassium": (150, 300), "Organic Carbon": (1, 2)},
    "Peppers": {"pH": (5.5, 7.0), "Nitrogen": (100, 200), "Phosphorus": (50, 100), "Potassium": (200, 400), "Organic Carbon": (1, 2)},
    "Rice": {"pH": (6.0, 7.5), "Nitrogen": (50, 150), "Phosphorus": (20, 60), "Potassium": (150, 300), "Organic Carbon": (1, 2)},
    "Maize": {"pH": (6.0, 7.5), "Nitrogen": (100, 200), "Phosphorus": (50, 100), "Potassium": (200, 300), "Organic Carbon": (1, 2)},
    "Sugarcane": {"pH": (5.5, 6.5), "Nitrogen": (100, 200), "Phosphorus": (50, 100), "Potassium": (200, 400), "Organic Carbon": (1, 2)},
    "Soybeans": {"pH": (6.0, 7.5), "Nitrogen": (50, 150), "Phosphorus": (20, 60), "Potassium": (150, 300), "Organic Carbon": (1, 2)},
    "Potatoes": {"pH": (5.0, 6.5), "Nitrogen": (100, 200), "Phosphorus": (50, 100), "Potassium": (200, 400), "Organic Carbon": (2, 3)},
    "Carrots": {"pH": (6.0, 7.0), "Nitrogen": (50, 150), "Phosphorus": (50, 100), "Potassium": (150, 300), "Organic Carbon": (2, 3)},
    "Lettuce": {"pH": (6.0, 6.5), "Nitrogen": (50, 150), "Phosphorus": (25, 75), "Potassium": (150, 300), "Organic Carbon": (1, 2)},
    "Broccoli": {"pH": (6.0, 7.0), "Nitrogen": (50, 150), "Phosphorus": (50, 100), "Potassium": (150, 300), "Organic Carbon": (2, 3)},
    "Cabbage": {"pH": (6.0, 7.0), "Nitrogen": (50, 150), "Phosphorus": (50, 100), "Potassium": (150, 300), "Organic Carbon": (2, 3)}
}
fertilizers = {
   
    "Urea": {"Nitrogen": 46, "Phosphorus": 0, "Potassium": 0},
    "Ammonium nitrate": {"Nitrogen": 34, "Phosphorus": 0, "Potassium": 0},
    "Superphosphate": {"Nitrogen": 0, "Phosphorus": 18, "Potassium": 0},
    "Triple superphosphate": {"Nitrogen": 0, "Phosphorus": 46, "Potassium": 0},
    "Monoammonium phosphate (MAP)": {"Nitrogen": 11, "Phosphorus": 52, "Potassium": 0},
    "Diammonium phosphate (DAP)": {"Nitrogen": 18, "Phosphorus": 46, "Potassium": 0},
    "Potassium nitrate": {"Nitrogen": 13, "Phosphorus": 0, "Potassium": 44},
    "Potassium chloride": {"Nitrogen": 0, "Phosphorus": 0, "Potassium": 60},
    "Ammonium sulfate": {"Nitrogen": 21, "Phosphorus": 0, "Potassium": 0},
    "Calcium ammonium nitrate (CAN)": {"Nitrogen": 15.5, "Phosphorus": 0, "Potassium": 0},
    "Magnesium ammonium phosphate": {"Nitrogen": 0, "Phosphorus": 16, "Potassium": 24},
    "20-20-20 NPK fertilizer": {"Nitrogen": 20, "Phosphorus": 20, "Potassium": 20},
    "16-16-16 NPK fertilizer": {"Nitrogen": 16, "Phosphorus": 16, "Potassium": 16},
    "10-26-26 NPK fertilizer": {"Nitrogen": 10, "Phosphorus": 26, "Potassium": 26},
    "10-20-30 NPK fertilizer": {"Nitrogen": 10, "Phosphorus": 20, "Potassium": 30}
    }
from sklearn import tree
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app,origin='http://localhost:3000')



# Training data
X = []
y = []

for crop, values in standards.items():
    X.append([
        values['pH'][0], values['pH'][1],
        values['Nitrogen'][0], values['Nitrogen'][1],
        values['Phosphorus'][0], values['Phosphorus'][1],
        values['Potassium'][0], values['Potassium'][1],
        values['Organic Carbon'][0], values['Organic Carbon'][1]
    ])
    y.append(crop)

# Create a decision tree classifier
clf = tree.DecisionTreeClassifier()
clf.fit(X, y)

def crop_recommender(pH, nitrogen, phosphorus, potassium, organic_carbon):
    # Predict the crop probabilities using the machine learning model
    crop_probs = clf.predict_proba([[pH, pH, nitrogen, nitrogen, phosphorus, phosphorus, potassium, potassium, organic_carbon, organic_carbon]])

    # Get the top 5 predicted crops along with their probabilities
    top_crops = list(sorted(zip(clf.classes_, crop_probs[0]), key=lambda x: x[1], reverse=True)[:5])

    print("The most suitable crops recommended by the Crop Recommender are:",top_crops)
    s=', '.join(top_crop[0] for top_crop in top_crops)
    return s




def nutrition_recommender(pH, nitrogen, phosphorus, potassium):
    results = {}
    for fertilizer, values in fertilizers.items():
        score = 0
        if pH >= 6.0 and pH <= 6.8:
            if nitrogen >= 50 and nitrogen <= 200:
                score += values["Nitrogen"]
            if phosphorus >= 50 and phosphorus <= 150:
                score += values["Phosphorus"]
            if potassium >= 200 and potassium <= 400:
                score += values["Potassium"]
        elif pH >= 6.0 and pH <= 7.5:
            if nitrogen >= 50 and nitrogen <= 150:
                score += values["Nitrogen"]
            if phosphorus >= 25 and phosphorus <= 75:
                score += values["Phosphorus"]
            if potassium >= 150 and potassium <= 300:
                score += values["Potassium"]
        if pH >= 5.5 and pH <= 7.0:
            if nitrogen >= 100 and nitrogen <= 200:
                score += values["Nitrogen"]
            if phosphorus >= 50 and phosphorus <= 100:
                score += values["Phosphorus"]
            if potassium >= 200 and potassium <= 400:
                score += values["Potassium"]
        results[fertilizer] = score
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)[:3]
    json_data = [{'name':item[0],'score':item[1]} for item in sorted_results]
    return json_data
    
def add_standard():
    crop = input("Enter the name of the crop: ")
    pH = tuple(map(float, input("Enter pH range (min, max): ").split(',')))
    nitrogen = tuple(map(float, input("Enter Nitrogen range (min, max): ").split(',')))
    phosphorus = tuple(map(float, input("Enter Phosphorus range (min, max): ").split(',')))
    potassium = tuple(map(float, input("Enter Potassium range (min, max): ").split(',')))
    organic_carbon = tuple(map(float, input("Enter Organic Carbon range (min, max): ").split(',')))
    standards[crop] = {"pH": pH, "Nitrogen": nitrogen, "Phosphorus": phosphorus, "Potassium": potassium, "Organic Carbon": organic_carbon}
    print(f"Standard for {crop} added successfully!")
def add_fertilizer():
    name = input("Enter the name of the fertilizer: ")
    nitrogen = float(input("Enter the nitrogen percentage: "))
    phosphorus = float(input("Enter the phosphorus percentage: "))
    potassium = float(input("Enter the potassium percentage: "))
    fertilizers[name] = {"Nitrogen": nitrogen, "Phosphorus": phosphorus, "Potassium": potassium}
    print(f"{name} added to the list of fertilizers.")
    

@app.route('/cropRecommender', methods=['POST'])
def predict():
    # Retrieve input data from the request
    data = request.get_json()['data']
    result = crop_recommender(data['pH'], data['nitrogen'],data['phosphorus'],data['potassium'],data['organic_carbon'])

    # Perform ML prediction using the data
    # ...

    # Return the ML prediction as a response
    prediction = {'msg':"success", 'result': result,'error':None}
    return jsonify(prediction)

@app.route('/fertiliser', methods=['POST'])
def fertiliser():
    # Retrieve input data from the request
    data = request.get_json()['data']
    result = nutrition_recommender(float(data['pH']), int(data['nitrogen']),int(data['phosphorus']),int(data['potassium']))

    # Perform ML prediction using the data
    # ...

    # Return the ML prediction as a response
    prediction = {'msg':"success", 'result': result,'error':None}
    return jsonify(prediction)

if __name__ == '__main__':
    app.run(debug=True)
# def main():
#     print("*********************************************")
#     print("****  WELCOME TO THE RECOMMENDER SYSTEM  ****")
#     print("*********************************************")
#     print("\n")
#     while True:
#         print("Please choose an option:")
#         print("1. Crop Recommender")
#         print("2. Nutrition Recommender")
#         print("3. Add a Crop Standard")
#         print("4. Add a Fertilizer")
#         print("5. Exit")
#         print("\n")
#         choice = input("Enter your choice (1, 2, 3, 4, or 5): ")
#         if choice == "1":
#             pH = float(input("Enter the pH value: "))
#             nitrogen = float(input("Enter the Nitrogen value: "))
#             phosphorus = float(input("Enter the Phosphorus value: "))
#             potassium = float(input("Enter the Potassium value: "))
#             organic_carbon = float(input("Enter the Organic Carbon value: "))
#             crop_recommender(pH, nitrogen, phosphorus, potassium, organic_carbon)
#             break
#         elif choice == "2":
#             pH = float(input("Enter the pH value: "))
#             nitrogen = float(input("Enter the Nitrogen value: "))
#             phosphorus = float(input("Enter the Phosphorus value: "))
#             potassium = float(input("Enter the Potassium value: "))
#             nutrition_recommender(pH, nitrogen, phosphorus, potassium)
#             break
#         elif choice == "3":
#             add_standard()
#             break
#         elif choice == "4":
#             add_fertilizer()
#             break
#         elif choice == "5":
#             print("*********************************************")
#             print("****  THANK YOU FOR USING! Do Visit us again!  ****")
#             print("*********************************************")
#             break
#         else:
#             print("Invalid choice. Please choose again.")

# main()