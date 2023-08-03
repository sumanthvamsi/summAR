def bart(vim,min_value,max_value):
    import textwrap
    from transformers import BartForConditionalGeneration, BartTokenizer

    import re
    from transformers import pipeline
    from transformers import BartTokenizer, BartForConditionalGeneration

    model_path = "/Users/buddy/Downloads/Summarizer-main/apps/home/test-dialogue-summarization/checkpoint-500"
    tokenizer = BartTokenizer.from_pretrained(model_path)
    model = BartForConditionalGeneration.from_pretrained(model_path)
    dialog_summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

    def chunk_paragraph(paragraph, max_chunk_length=800):
        # Split the paragraph into words
        words = re.findall(r'\w+', paragraph)

        # Initialize variables
        chunks = []
        current_chunk = []

        # Iterate through the words
        for word in words:
            current_chunk.append(word)

            # Check if the current chunk length exceeds the maximum length
            if len(current_chunk) >= max_chunk_length:
                chunks.append(' '.join(current_chunk))
                current_chunk = []

        # Add the last chunk (if any)
        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

    # Function to summarize a given text using the summarization model
    def summarize_text(input_string):
        result = dialog_summarizer(input_string, min_length=min_value, max_length=max_value)
        summary=result[0]['summary_text']
        return summary

    def fsummarize_text(input_string):
        result = dialog_summarizer(input_string, min_length=min_value, max_length=max_value)
        summary=result[0]['summary_text']
        return summary

    input_string = vim
    temp=1
    temps=1

        # Split the input string into parts
    split_parts = chunk_paragraph(input_string)

        # Initialize a list to store the summaries of each chunk
    summaries = []

        # Summarize each chunk using the summarization model
    for part in split_parts:
        print(part)
        summary = summarize_text(part)
        summaries.append(summary)
        temps+=1
        print(temps)

        # Combine all the summaries into a single text
    combined_summary = " ".join(summaries)

        # Summarize the combined summary
    final_summary = fsummarize_text(combined_summary)

    print("Final Summary:")
    print(final_summary)
    return final_summary