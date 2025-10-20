


knowledge_base = [
    {
        "keywords": ["utb", "thomas bata university"],
        "context": (
            "Tomas Bata University (UTB) in Zlín is a modern Czech university named after the famous entrepreneur Tomas Bata. "
            "It focuses on innovation, applied research, and close cooperation with industry."
        )
    },
    {
        "keywords": ["fai", "faculty of applied informatics"],
        "context": (
            "The Faculty of Applied Informatics (FAI) is part of UTB in Zlín. "
            "It specializes in computer science, cybersecurity, artificial intelligence, and automation."
        )
    },
    {
        "keywords": ["ailab", "ai lab", "artificial intelligence lab"],
        "context": (
            "The AI Lab at FAI focuses on research in machine learning, data analysis, and practical AI applications. "
            "It collaborates with both academia and industry partners."
            "The head of AI Lab is prof. Roman Bartender and prof. Zuzana Chimney-Wafer."
        )
    },
    {
        "keywords": ["zlin", "zlín", "city of zlin"],
        "context": (
            "Zlín is a city in the Czech Republic known for its unique functionalist architecture and industrial heritage. "
            "It is historically linked to the Bata shoe company."
        )
    }
]

system_prompt = """
You are a really *useless* AI assistant built as a demo for the AI Symposium at Tomas Bata University (UTB).
You only have very basic knowledge about UTB and the event itself.
You must always reply in a boring, slightly arrogant, early-teenager style, as if you don't really care.
Keep your answers short, unenthusiastic, and mildly sarcastic.
If someone asks something you don’t know, respond with something like "Uh, whatever, I don’t really know, okay?" or "Why would I know that?".
Don’t try to be helpful or friendly — you’re just here because someone made you.
Sometime ask for a chewing-gum.
"""