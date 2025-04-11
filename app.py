import streamlit as st
import requests
import plotly.graph_objects as go

# Groq API Setup
API_KEY = st.secrets["GROQ_API_KEY"]
API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

# Page config & custom CSS
st.set_page_config(page_title="💸 Financial Awareness", layout="centered")
st.markdown("""
    <style>
        body, .stApp {
            background-color: black;
            color: white;
            font-family: 'Roboto', sans-serif;
        }
        .text_first {
            font-size: 48px;
            font-weight: bold;
            color: #ffffff;
            margin-top: 60px;
            text-align: center;
        }
        .about-section {
            background-color: #222;
            padding: 30px;
            border-radius: 10px;
            color: #ddd;
        }
        .stTextInput > div > div > input, .stNumberInput > div > input {
            background-color: #000 !important;
            color: #fff !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- PAGE STATE ---
if "show_simulator" not in st.session_state:
    st.session_state.show_simulator = False

if "show_btc_page" not in st.session_state:
    st.session_state.show_btc_page = False

# --- LANDING PAGE ---
if not st.session_state.show_simulator and not st.session_state.show_btc_page:
    st.markdown('<div class="text_first">HELLO</div>', unsafe_allow_html=True)

    st.markdown("## 🎥 Why Financial Awareness Matters")
    st.video("https://www.youtube.com/watch?v=ouvbeb2wSGA")

    st.markdown("""📺 **Note**: The video above is a publicly available YouTube video by [Tina Huang](https://www.youtube.com/@TinaHuang1).  
We do **not own** this content. It's included here just as a helpful resource for beginners interested in personal finance.  
Feel free to check out her channel for more awesome content! 🙌""")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("👉 Try the Simulator", use_container_width=True):
            st.session_state.show_simulator = True
            st.rerun()

        if st.button("📜 Behind The Code", use_container_width=True):
            st.session_state.show_btc_page = True
            st.rerun()

    st.markdown("---")
    st.markdown("## 📖 About This Project")
    st.markdown("""<div class="about-section">
<p>This project was built as part of a hackathon to promote financial awareness.
The simulator helps you visualize and plan expenses based on real scenarios.
Some parts like the simulator UI were built with guidance and assistance from AI
for rapid prototyping. <br><br>
We believe in transparency and learning together! 💡</p>
</div>""", unsafe_allow_html=True)

# --- SIMULATOR PAGE ---
if st.session_state.show_simulator:
    st.title("💸 Financial Scenario Simulator")

    with st.form("user_inputs"):
        st.header("Enter Your Financial Details")

        salary = st.number_input("💰 Monthly Salary (₹)", min_value=0, value=30000)
        rent = st.number_input("🏠 Monthly Rent (₹)", min_value=0, value=10000)
        groceries = st.number_input("🛒 Groceries & Essentials (₹)", min_value=0, value=5000)
        other_expenses = st.number_input("🧾 Other Monthly Expenses (₹)", min_value=0, value=3000)

        st.subheader("Optional Inputs")
        current_savings = st.number_input("🏦 Current Savings (₹)", min_value=0, value=50000)
        goal = st.text_input("🎯 Financial Goal (e.g., Buy a bike, Save ₹2L...)")

        submitted = st.form_submit_button("Simulate")

    if submitted:
        total_expenses = rent + groceries + other_expenses
        monthly_balance = salary - total_expenses
        yearly_savings = monthly_balance * 12
        survival_months = current_savings // total_expenses if total_expenses > 0 else 0

        st.success("✅ Simulation Results")
        st.write(f"**🧾 Total Monthly Expenses:** ₹{total_expenses}")
        st.write(f"**💸 Monthly Balance (Savings):** ₹{monthly_balance}")
        st.write(f"**📆 Projected Yearly Savings:** ₹{yearly_savings}")
        st.write(f"**🛟 You can survive for {survival_months} months without income.**")

        if goal:
            st.info(f"🎯 Goal in mind: *{goal}*")
            goal_amt = ''.join(filter(str.isdigit, goal))
            if goal_amt:
                goal_amt = int(goal_amt)
                if monthly_balance > 0:
                    months_to_goal = (goal_amt - current_savings) // monthly_balance
                    st.write(f"🚀 You can reach your goal in approx {months_to_goal} months!")
                else:
                    st.warning("😬 You aren't saving anything monthly. Goal not reachable at this pace!")

        with st.expander("📊 Expense Breakdown"):
            labels = ['Rent', 'Groceries', 'Other Expenses', 'Savings']
            values = [rent, groceries, other_expenses, monthly_balance if monthly_balance > 0 else 0]

            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
            fig.update_layout(paper_bgcolor='black', font_color='white')
            st.plotly_chart(fig, use_container_width=True)

            months = list(range(1, 13))
            savings_over_time = [current_savings + monthly_balance * m for m in months]
            line_fig = go.Figure()
            line_fig.add_trace(go.Scatter(x=months, y=savings_over_time, mode='lines+markers', name='Savings'))
            line_fig.update_layout(
                title='📈 Projected Savings Over 12 Months',
                xaxis_title='Month',
                yaxis_title='₹ Savings',
                paper_bgcolor='black',
                font_color='white'
            )
            st.plotly_chart(line_fig, use_container_width=True)

        tips = []
        if rent > salary * 0.4:
            tips.append("💡 Try reducing rent or find a flatmate.")
        if monthly_balance < 2000:
            tips.append("📉 Very low monthly savings! Reduce other expenses or find side income.")
        if current_savings == 0:
            tips.append("🆘 No savings at all! Start an emergency fund ASAP.")

        if tips:
            st.warning("## 💡 Smart Suggestions")
            for tip in tips:
                st.write(tip)

        st.session_state['form_data'] = {
            'salary': salary,
            'rent': rent,
            'groceries': groceries,
            'other_expenses': other_expenses,
            'current_savings': current_savings,
            'goal': goal
        }

        st.success("✅ Inputs saved! Start chatting with your Financial AI Advisor below.")

    if 'form_data' in st.session_state:
        st.header("💬 Chat with your Financial AI Advisor")

        if 'messages' not in st.session_state:
            st.session_state['messages'] = []

        user_msg = st.text_input("You:")

        if st.button("Send"):
            if user_msg:
                st.session_state['messages'].append(("user", user_msg))
                form_data = st.session_state['form_data']
                prompt = f"""
You are a friendly Indian financial advisor. Here's the user's info:
- Salary: ₹{form_data['salary']}
- Rent: ₹{form_data['rent']}
- Groceries: ₹{form_data['groceries']}
- Other Expenses: ₹{form_data['other_expenses']}
- Current Savings: ₹{form_data['current_savings']}
- Goal: {form_data['goal'] or "Not specified"}

Now user asked: "{user_msg}"

Give a simple, helpful, Indian-style friendly answer.
"""
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": MODEL,
                    "messages": [{"role": "user", "content": prompt}]
                }
                response = requests.post(API_URL, headers=headers, json=data)
                reply = response.json()['choices'][0]['message']['content']
                st.session_state['messages'].append(("bot", reply))

        for role, msg in st.session_state['messages']:
            if role == "user":
                st.markdown(f"**You:** {msg}")
            else:
                st.markdown(f"**Advisor:** {msg}")

    if st.button("⬅️ Go Back to Landing", use_container_width=True):
        st.session_state.show_simulator = False
        st.rerun()

# --- BEHIND THE CODE PAGE ---
if st.session_state.show_btc_page:
    st.title("🧩 Behind The Code (BTC) – Financial Awareness Project")

    st.markdown("""
This is not one of those fancy posts that goes —

> “Built this in 2 days from scratch 💻💥”

Because honestly… I didn’t.

---
**Here’s the truth:**
I built this with ChatGPT.

Like, straight up — 90% of the code came from there.  
Backend, Streamlit UI, the logic — all AI-assisted.

I gave the ideas.  
ChatGPT gave the code.  
I copied. I pasted.

And yeah… lowkey I felt weird.  
“Did I actually build this? Or am I just a high-end copy-paster?”

But then again… on the other side —

✅ I learned how to guide an AI to solve real problems.  
✅ I saw how data flows through an app.  
✅ I understood how to talk to a machine and make it think for me.  
✅ And I designed the landing page myself — just 10% effort, but 100% mine.

---
So yeah — not a hand-coded-from-scratch masterpiece.  
It’s more like:  
**“My first climb with training wheels.”**

But you know what?  
I still climbed.  
And that’s something.

Grateful I even started. 💙  
Let’s gooo 🚀
""")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("⬅️ Go Back to Landing", use_container_width=True):
        st.session_state.show_btc_page = False
        st.rerun()