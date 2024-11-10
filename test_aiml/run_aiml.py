import aiml

# Create the kernel and learn the AIML file
kernel = aiml.Kernel()
kernel.learn("main.aiml")

# Enter a loop to chat
print("Chatbot is ready! Type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    response = kernel.respond(user_input)
    print("Bot:", response)
