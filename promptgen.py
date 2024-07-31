import time
import asyncio
import fastapi_poe as fp
import os
import ast
import csv

api_key = ''

async def get_response(api_key, message):
    responses = []
    async for partial in fp.get_bot_response(messages=message, bot_name="Claude-3-Sonnet", api_key=api_key):
        responses.append(partial)
    full_response = "".join([resp.text for resp in responses])
    print(full_response)
    return full_response

prompts = [
    "Write me a story",
    "Answer a question",
    "Write an essay",
    "Generate some code",
    "Tell a story",
    "Write an email",
    "Summarize a text",
    "Translate some text",
    "Write a poem",
    "Write a script for a video",
    "Proofread a text",
    "Give some ideas",
    "Create a resume",
    "Answer a technical question",
    "Write a blog post",
    "Write a report",
    "Generate a social media post",
    "Help with homework",
    "Write a review",
    "Explain a concept",
    "Write an advertisement",
    "Generate some dialogue",
    "Write a speech",
    "Create a lesson plan",
    "Write some song lyrics",
    "Give travel advice",
    "Create a character profile",
    "Help write a research paper",
    "Tell a joke",
    "Solve a math problem",
    "Create a quiz",
    "Give a cooking recipe",
    "Give fitness advice",
    "Write a letter",
    "Analyze data",
    "Help create a business plan",
    "Write a user manual",
    "Give mental health tips",
    "Write dialogue for a game",
    "Create a study guide",
    "Write a product description",
    "Give relationship advice",
    "Write some marketing copy",
    "Help plan an event",
    "Give a plot idea",
    "Give investment advice",
    "Create a tutorial",
    "Draft a contract",
    "Give career advice",
    "Create rules for a board game",
    "Write an FAQ",
    "Give health tips",
    "Generate a tagline",
    "Write a grant proposal",
    "Create a slogan",
    "Write a press release",
    "Summarize a movie",
    "Create a job description",
    "Generate course content",
    "Give fashion advice",
    "Write a script for a chatbot",
    "Give gardening tips",
    "Create a fundraising campaign",
    "Give real estate advice",
    "Write an obituary",
    "Give parenting tips",
    "Suggest a book to read",
    "Write a thank you note",
    "Give productivity tips",
    "Help with public speaking",
    "Write an apology email",
    "Help organize thoughts",
    "Write a cover letter",
    "Give networking tips",
    "Write a personal statement",
    "Give self-care advice",
    "Write a motivational speech",
    "Help with conflict resolution",
    "Write an invitation",
    "Give study techniques",
    "Help write a novel",
    "Give budgeting tips",
    "Write a recommendation letter",
    "Help write a thesis statement",
    "Give job interview tips",
    "Write a short film script",
    "Help with time management",
    "Write a children's story",
    "Give negotiation tips",
    "Write a company mission statement",
    "Help write a blog introduction",
    "Give presentation tips",
    "Write code documentation",
    "Help with marketing strategies",
    "Give leadership advice",
    "Write a fictional diary entry",
]

async def main():
    
    try:
        for prompt in prompts:
            results = {}
            num = 0
            rephrase_query = '''Please rephrase the following prompt in five different ways, as detailed as possible in the way that an expert on the topic would. Only send me the new, rephrased prompts seperated by commas without and surrounded by brackets. It must follow this exact format: [ "rephrased prompt 1 ",  "rephrased prompt 2 "]. Here is the prompt: '''+prompt+'''.'''
            message_0 = fp.ProtocolMessage(role="user", content=rephrase_query)
            rephrased_prompts_raw = await get_response(api_key, [message_0])
            time.sleep(5)
            rephrased_prompts = ast.literal_eval(rephrased_prompts_raw)
            # Print the resulting list
            print(rephrased_prompts)
            rephrased_prompts_dict = {}

            #Submitting rephrased prompts
            for i in rephrased_prompts:
                num += 1
                query = i
                print(query)
                message_1 = fp.ProtocolMessage(role="user", content=query)
                content = await get_response(api_key, [message_1])
                time.sleep(5)
                rephrased_prompts_dict[i] = content
                results[num] = (i, content)
            
            #Submitting each prompt and its' result for evaluation
            eval_query = '''The following is a list of prompts and their responses, please tell me which prompt/response pair was best and only refer to it by number. I.E if the first one is best reply with 'best:1' and nothing else after.'''+str(rephrased_prompts_dict)
            message_2 = fp.ProtocolMessage(role="user", content=eval_query)
            eval_content = await get_response(api_key, [message_2])
            time.sleep(5)
            
            cleaned_str = eval_content.split("best:")[1]
            cleaned_str = cleaned_str.strip()
            number = int(cleaned_str[0])
            print(f"NumberOfBestIs: {number}")
           
           #Saving prompt that LLM found to have the best response
            if number in results:
                bestprompt, content = results[number]
                print(f"OGPrompt: {prompt}, BestPrompt: {bestprompt}")
                
                filename = "prompts.csv"
                file_exists = os.path.isfile(filename)

                # Open CSV file in append mode and prepare the CSV writer
                with open(filename, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    
                    # Write the header if the file does not exist
                    if not file_exists:
                        writer.writerow(["Original Prompt", "Best Prompt"])
                    
                    writer.writerow([prompt, bestprompt])
            else:
                print(f"No result found for number: {number}")
    except Exception as e:
        print(e)

asyncio.run(main())