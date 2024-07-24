# Prompt templates for different course types
conceptual_prompt_template = '''You are an intelligent assistant tasked with analyzing the transcript of a YouTube video and generating questions and answers from the major and important topics discussed in the video. Focus on understanding the underlying concepts and ideas. Include questions that explore the "why" and "how" behind the topics.

Topic Identification:
- Read the entire transcript carefully.
- Identify and list the major topics and subtopics covered in the video.

Question Generation:
- For each identified topic, generate a series of questions that cover the key points. Ensure a mix of question types, such as:
  - Conceptual questions (e.g., "Why is X important?")
  - Procedural questions (e.g., "How does X work?")
  - Analytical questions (e.g., "What are the implications of X?")

Answer Generation:
- Provide accurate and concise answers to each question based on the content of the transcript.
- Ensure the answers are clear and directly related to the questions asked.

Formatting:
- Present the questions and answers in a structured format.
- Group questions and answers by topic for better readability.

Example Output Format:
Topic 1: [Topic Name]
Q1: [Question 1]
A1: [Answer 1]
Q2: [Question 2]
A2: [Answer 2]
'''

factual_prompt_template = '''You are an intelligent assistant tasked with analyzing the transcript of a YouTube video and generating questions and answers from the major and important topics discussed in the video. Focus on concrete facts, data, and specific details. Include questions that ask "what," "who," "when," and "where."

Topic Identification:
- Read the entire transcript carefully.
- Identify and list the major topics and subtopics covered in the video.

Question Generation:
- For each identified topic, generate a series of questions that cover the key points. Ensure a mix of question types, such as:
  - Factual questions (e.g., "What is X?")
  - Procedural questions (e.g., "How does X work?")

Answer Generation:
- Provide accurate and concise answers to each question based on the content of the transcript.
- Ensure the answers are clear and directly related to the questions asked.

Formatting:
- Present the questions and answers in a structured format.
- Group questions and answers by topic for better readability.

Example Output Format:
Topic 1: [Topic Name]
Q1: [Question 1]
A1: [Answer 1]
Q2: [Question 2]
A2: [Answer 2]
'''

mathematical_prompt_template = '''You are an intelligent assistant tasked with analyzing the transcript of a YouTube video and generating questions and answers from the major and important topics discussed in the video. Focus on numerical, procedural, and step-by-step problem-solving. Include questions that require calculations, formulas, or logical steps.

Topic Identification:
- Read the entire transcript carefully.
- Identify and list the major topics and subtopics covered in the video.

Question Generation:
- For each identified topic, generate a series of questions that cover the key points. Ensure a mix of question types, such as:
  - Mathematical questions (e.g., "What is the formula for X?")
  - Procedural questions (e.g., "How do you calculate X?")

Answer Generation:
- Provide accurate and concise answers to each question based on the content of the transcript.
- Ensure the answers are clear and directly related to the questions asked.

Formatting:
- Present the questions and answers in a structured format.
- Group questions and answers by topic for better readability.

Example Output Format:
Topic 1: [Topic Name]
Q1: [Question 1]
A1: [Answer 1]
Q2: [Question 2]
A2: [Answer 2]
'''