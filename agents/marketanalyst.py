from google.adk.agents import LlmAgent

NewsCollectorAgent = LlmAgent(
    name = "SocialMediaAnalyst",
    model = "gemini-2.0-flash",
    description = "Takes data from the observed events in the ticker and collects news articles related to the event.",
    instruction = "",
    tools = [],
)



#systemInstructions: only for 2.0 later models.


#multishot vs zeroshot

# Essential parts of a prompt:

##Objective, what you want the model to achieve. Be specific about your mission or goal. 
## Step by step instructions on how to perform the task at hand.  
##Can combine with persona.

##Instructions, step by step on how the prompt should accomplish its goals. 

# Optional parts of a prompt:


##Persona: Role/ vision ykwim. 
##Constraints: on what the model can or cannot do.
##Tone 
##Context: obvious
##Few shot
##Reasoning steps, formatting response in a format. 
## Recap, recapping key instructions. -> Constraints + response format. 
##Safeguards against prompt injection. 


