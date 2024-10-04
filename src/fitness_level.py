def calculate_bmi(weight, height):
    bmi = weight / ((height/100) ** 2)
    return round(bmi, 2)

def determine_fitness_level(bmi, age):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"