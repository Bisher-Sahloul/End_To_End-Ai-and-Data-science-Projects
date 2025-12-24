
from processor_bert import classify_with_bert
from processor_llm import classify_with_llm
from processor_regex import classify_with_regex



def classify_logs(source , log_message):
    if source == "LegacyCRM":
        return classify_with_llm(log_message)
    label = classify_with_regex(log_message)
    if label is not None : 
        return label
    return classify_with_bert(log_message)



def classify(logs):
    labels = []
    for source , log_message in logs : 
        labels.append(classify_logs(source , log_message))
    return labels



def classify_csv(input_file):
    import pandas as pd
    df = pd.read_csv(input_file)

    # Perform classification
    df["target_label"] = classify(list(zip(df["source"], df["log_message"])))

    # Save the modified file
    output_file = "output.csv"
    df.to_csv(output_file, index=False)

    return output_file

