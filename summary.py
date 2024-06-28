from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, TFAutoModelForSeq2SeqLM, DPRReader, DPRReaderTokenizer
from youtube_extraction import preprocessed_text

# Use TensorFlow-compatible model for sequence-to-sequence learning
generator = TFAutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")
generator_tokenizer = AutoTokenizer.from_pretrained("facebook/bart-base")

tokenized_text = generator_tokenizer.batch_encode_plus([preprocessed_text], max_length=512, truncation=True, return_tensors="tf")

generator_input = {
    "input_ids": tokenized_text["input_ids"],
    "attention_mask": tokenized_text["attention_mask"],
}

# Generate summary
summary_output = generator.generate(**generator_input)

segment_length = 300
segments = [preprocessed_text[i:i+segment_length] for i in range(0, len(preprocessed_text), segment_length)]

summary_texts = []
for segment in segments:
    tokenized_segment = generator_tokenizer.batch_encode_plus([segment], max_length=512, truncation=True, return_tensors="tf")
    segment_input = {
        "input_ids": tokenized_segment["input_ids"],
        "attention_mask": tokenized_segment["attention_mask"],
    }
    segment_summary_output = generator.generate(**segment_input)
    segment_summary_text = generator_tokenizer.batch_decode(segment_summary_output, skip_special_tokens=True)[0]
    summary_texts.append(segment_summary_text)

full_summary_text = " ".join(summary_texts)

print("Full Summary of the YouTube video:")
print(full_summary_text)
