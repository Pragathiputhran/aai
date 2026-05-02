import streamlit as st
import wikipedia
from fpdf import FPDF

# ---------------- MEMORY ----------------
class Memory:
    def __init__(self):
        self.data = []

    def store(self, info):
        self.data.append(info)

    def retrieve(self):
        return self.data


# ---------------- TOOLS ----------------
def search_wikipedia(query):
    try:
        return wikipedia.summary(query, sentences=5)
    except:
        return "No data found"


# ---------------- EVALUATOR ----------------
def evaluate_content(content):
    return len(content) > 50


# ---------------- REPORT GENERATOR ----------------
def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in content.split("\n"):
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output("report.pdf")


# ---------------- AGENT ----------------
class Agent:
    def __init__(self):
        self.memory = Memory()

    def plan(self, goal):
        return [
            f"Search information about {goal}",
            f"Summarize key points of {goal}",
            f"Generate structured report on {goal}"
        ]

    def execute(self, task):
        if "Search" in task:
            return search_wikipedia(task)
        elif "Summarize" in task:
            return "Summary:\n" + search_wikipedia(task)
        elif "Generate" in task:
            memory_data = "\n".join(self.memory.retrieve())
            return f"Final Report:\n{memory_data}"

    def run(self, goal):
        tasks = self.plan(goal)
        final_output = ""

        for task in tasks:
            result = self.execute(task)

            if evaluate_content(result):
                self.memory.store(result)
                final_output += result + "\n\n"
            else:
                refined = "Refined: " + result
                self.memory.store(refined)
                final_output += refined + "\n\n"

        return final_output


# ---------------- STREAMLIT UI ----------------
st.title("Agentic AI Research Assistant")

topic = st.text_input("Enter Topic")

if st.button("Generate Report"):
    agent = Agent()
    output = agent.run(topic)

    st.subheader("Generated Output")
    st.write(output)

    generate_pdf(output)

    with open("report.pdf", "rb") as f:
        st.download_button("Download Report", f, "report.pdf")
