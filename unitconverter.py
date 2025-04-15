import streamlit as st


def Calculation_function(big_type, small_type, conver_type, input_value):
    if small_type == conver_type:
        return input_value  # No conversion needed
    
    # Conversion factors for different units
    conversion_factors = {
        "Time": {
            "Second (s)": 1,
            "Minute (min)": 60,
            "Hour (h)": 3600,
            "Day (d)": 86400,
            "Week": 604800,
            "Month": 2.628e+6,  # Approximate
            "Year": 3.154e+7  # Approximate
        },
        "Length": {
            "Nanometer (nm)": 1e-9,
            "Micrometer (µm)": 1e-6,
            "Millimeter (mm)": 1e-3,
            "Centimeter (cm)": 1e-2,
            "Meter (m)": 1,
            "Kilometer (km)": 1e3,
            "Mile (mi)": 1609.34
        },
        "Mass": {
            "Milligram (mg)": 1e-3,
            "Gram (g)": 1,
            "Kilogram (kg)": 1e3,
            "Metric Ton (t)": 1e6
        },
        "Area": {
            "Square Millimeter (mm²)": 1e-6,
            "Square Centimeter (cm²)": 1e-4,
            "Square Meter (m²)": 1,
            "Square Kilometer (km²)": 1e6
        },
        "Speed": {
            "Meters per Second (m/s)": 1,
            "Kilometers per Hour (km/h)": 0.277778,
            "Miles per Hour (mph)": 0.44704
        },
        "Frequency": {
            "Hertz (Hz)": 1,
            "Kilohertz (kHz)": 1e3,
            "Megahertz (MHz)": 1e6,
            "Gigahertz (GHz)": 1e9
        },
        "Digital Storage": {
            "Bit": 1,
            "Byte": 8,
            "Kilobyte (KB)": 8e3,
            "Megabyte (MB)": 8e6,
            "Gigabyte (GB)": 8e9,
            "Terabyte (TB)": 8e12,
            "Petabyte (PB)": 8e15
        },
        "Plane Angle": {
            "Gradian (gon)": 0.9,
            "Degree (°)": 1,
            "Radian (rad)": 57.2958
        }
    }

    # Handle Temperature separately since it's not a direct multiplication
    if big_type == "Temperature":
        if small_type == "Celsius (°C)" and conver_type == "Fahrenheit (°F)":
            return round((input_value * 9/5) + 32, 2)
        elif small_type == "Fahrenheit (°F)" and conver_type == "Celsius (°C)":
            return round((input_value - 32) * 5/9, 2)
        else:
            return "Invalid Temperature Conversion"

    # Ensure valid conversion types
    if big_type in conversion_factors:
        if small_type in conversion_factors[big_type] and conver_type in conversion_factors[big_type]:
            # Convert input to base unit (e.g., meters, grams, seconds)
            input_in_base_unit = input_value * conversion_factors[big_type][small_type]
            # Convert from base unit to desired output
            output_value = input_in_base_unit / conversion_factors[big_type][conver_type]
            return output_value # Round for better readability

    return "Invalid Conversion"
        

st.set_page_config("Unit Converter",page_icon="⏳", layout="wide" )
# Dropdown list
options = [
    "Area",
    "Digital Storage",
    "Frequency",
    "Length",
    "Mass",
    "Plane Angle",
    "Speed",
    "Temperature",
    "Time"
]


unit_conversions = {
    "Area": ["Square Millimeter (mm²)", "Square Centimeter (cm²)", "Square Meter (m²)", "Square Kilometer (km²)"],

    "Digital Storage": ["Bit", "Byte", "Kilobyte (KB)", "Megabyte (MB)", "Gigabyte (GB)", "Terabyte (TB)", "Petabyte (PB)"],

    "Frequency": ["Hertz (Hz)", "Kilohertz (kHz)", "Megahertz (MHz)", "Gigahertz (GHz)"],

    "Length": ["Nanometer (nm)", "Micrometer (µm)", "Millimeter (mm)", "Centimeter (cm)", 
               "Meter (m)", "Kilometer (km)", "Mile (mi)"],

    "Mass": ["Milligram (mg)", "Gram (g)", "Kilogram (kg)", "Metric Ton (t)"],

    "Plane Angle": ["Gradian (gon)", "Degree (°)", "Radian (rad)"],

    "Speed": ["Meters per Second (m/s)", "Kilometers per Hour (km/h)", "Miles per Hour (mph)"],

    "Temperature": ["Celsius (°C)", "Fahrenheit (°F)"],

    "Time": ["Second (s)", "Minute (min)", "Hour (h)", "Day (d)", "Week", "Month", "Year"]
}



selected_option = st.selectbox("Units", options)

col1,col2 = st.columns(2)

with col1:
    st.subheader("Input Area")
    current_input_style = st.selectbox("Current Input",unit_conversions[selected_option])
    myinput = st.number_input("Enter your Unit value:")

with col2:
    st.subheader("Output Area")
    current_output= st.selectbox("Output Unit",unit_conversions[selected_option])
    st.text_input("Output value",Calculation_function(selected_option,current_input_style,current_output,myinput),disabled= True)
    
