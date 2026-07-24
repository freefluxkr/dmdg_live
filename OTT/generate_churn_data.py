import os
import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)

# Ensure OTT directory exists
ott_dir = os.path.dirname(os.path.abspath(__file__))
os.makedirs(ott_dir, exist_ok=True)

print("Starting OTT churn datasets generation...")

# ==========================================
# 1. Generate netflix_customer_churn.csv
# ==========================================
num_netflix_records = 5000

customer_ids = np.arange(1, num_netflix_records + 1)
ages = np.random.randint(18, 71, size=num_netflix_records)
genders = np.random.choice(["Male", "Female"], size=num_netflix_records)
regions = np.random.choice(["North America", "Europe", "Asia", "South America"], size=num_netflix_records)
devices = np.random.choice(["Smart TV", "Mobile", "Desktop", "Tablet"], size=num_netflix_records)

# Subscription tiers and associated costs
sub_types = np.random.choice(["Basic", "Standard", "Premium"], size=num_netflix_records, p=[0.4, 0.4, 0.2])
monthly_fees = []
for st in sub_types:
    if st == "Basic":
        monthly_fees.append(9.99)
    elif st == "Standard":
        monthly_fees.append(15.49)
    else:
        monthly_fees.append(19.99)
monthly_fees = np.array(monthly_fees)

tenure_months = np.random.randint(1, 25, size=num_netflix_records)
last_login_days = np.random.randint(0, 31, size=num_netflix_records)

# Watch hours correlates slightly with subscription type (Premium users watch more)
watch_hours = np.zeros(num_netflix_records)
for i in range(num_netflix_records):
    if sub_types[i] == "Premium":
        watch_hours[i] = np.random.uniform(40, 160)
    elif sub_types[i] == "Standard":
        watch_hours[i] = np.random.uniform(20, 120)
    else:
        watch_hours[i] = np.random.uniform(5, 80)

# Churn logic: churn probability is higher if watch hours are low and last login is high
churn_prob = 1.0 / (1.0 + np.exp(
    -1.5 * (50.0 - watch_hours) / 30.0 + 
    1.2 * (last_login_days - 10) / 10.0 - 
    0.5 * (tenure_months - 6) / 12.0
))
# Clip probability to realistic bounds [0, 1]
churn_prob = np.clip(churn_prob, 0.01, 0.99)
churned = np.random.binomial(1, churn_prob)

netflix_df = pd.DataFrame({
    "Customer_ID": customer_ids,
    "Age": ages,
    "Gender": genders,
    "Region": regions,
    "Subscription_Type": sub_types,
    "Monthly_Fee": monthly_fees,
    "Tenure_Months": tenure_months,
    "Watch_Hours": np.round(watch_hours, 1),
    "Last_Login_Days": last_login_days,
    "Device": devices,
    "Churned": churned
})

netflix_path = os.path.join(ott_dir, "netflix_customer_churn.csv")
netflix_df.to_csv(netflix_path, index=False)
print(f"Generated Netflix Churn Dataset: {netflix_path} (Shape: {netflix_df.shape})")


# ==========================================
# 2. Generate ott_churn_modeling.csv
# ==========================================
num_ott_records = 3000

user_ids = np.arange(10001, 10001 + num_ott_records)
ott_ages = np.random.randint(18, 76, size=num_ott_records)
ott_genders = np.random.choice(["Male", "Female"], size=num_ott_records)
sub_duration = np.random.randint(1, 37, size=num_ott_records)
monthly_charge = np.round(np.random.uniform(5.0, 25.0, size=num_ott_records), 2)
watch_time_weekly = np.round(np.random.exponential(scale=15.0, size=num_ott_records) + 1.0, 1)
# cap watch time at 80 hours per week
watch_time_weekly = np.clip(watch_time_weekly, 1.0, 80.0)

multi_screen = np.random.choice(["Yes", "No"], size=num_ott_records, p=[0.6, 0.4])
support_inquiries = np.random.poisson(lam=1.2, size=num_ott_records)
genre_pref = np.random.choice(["Action", "Comedy", "Drama", "Sci-Fi"], size=num_ott_records)

# Churn logic: Churn correlates with high support inquiries, low weekly watch time, and multi-screen usage
ott_churn_prob = 1.0 / (1.0 + np.exp(
    -2.0 * (15.0 - watch_time_weekly) / 10.0 + 
    1.5 * (support_inquiries - 1.5) - 
    0.8 * (1 if multi_screen == "Yes" else 0)
))
ott_churn_prob = np.clip(ott_churn_prob, 0.02, 0.98)
ott_churn = np.random.binomial(1, ott_churn_prob)

ott_df = pd.DataFrame({
    "User_ID": user_ids,
    "Age": ott_ages,
    "Gender": ott_genders,
    "Subscription_Duration_Months": sub_duration,
    "Monthly_Charge": monthly_charge,
    "Watch_Time_Weekly_Hours": watch_time_weekly,
    "Multi_Screen_Usage": multi_screen,
    "Customer_Support_Inquiries": support_inquiries,
    "Genre_Preference": genre_pref,
    "Churn": ott_churn
})

ott_path = os.path.join(ott_dir, "ott_churn_modeling.csv")
ott_df.to_csv(ott_path, index=False)
print(f"Generated OTT Churn Modeling Dataset: {ott_path} (Shape: {ott_df.shape})")

print("All datasets generated successfully!")
