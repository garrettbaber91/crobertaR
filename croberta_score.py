import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAMES = [
    "garrettbaber/twitter-roberta-base-joy-intensity",
    "garrettbaber/twitter-roberta-base-fear-intensity",
    "garrettbaber/twitter-roberta-base-anger-intensity",
    "garrettbaber/twitter-roberta-base-sadness-intensity",
]

EMOTIONS = ["Joy", "Fear", "Anger", "Sadness"]

_tokenizers = None
_models = None
_device = None

def _init_models():
    global _tokenizers, _models, _device

    if _tokenizers is not None and _models is not None and _device is not None:
        return

    _tokenizers = [AutoTokenizer.from_pretrained(n) for n in MODEL_NAMES]
    _models     = [AutoModelForSequenceClassification.from_pretrained(n) for n in MODEL_NAMES]

    if torch.backends.mps.is_available():
        _device = torch.device("mps")
    elif torch.cuda.is_available():
        _device = torch.device("cuda")
    else:
        _device = torch.device("cpu")

    for m in _models:
        m.to(_device)
        m.eval()

def score_df(df, batch_size=64, text_col="text", id_col="SubjectID", max_length=128):
    _init_models()

    if text_col not in df.columns:
        raise ValueError(f"Missing required column: {text_col}")

    df = df.dropna(subset=[text_col]).reset_index(drop=False)

    has_id = id_col in df.columns

    all_chunks = []
    with torch.no_grad():
        for start in range(0, len(df), batch_size):
            batch = df.iloc[start:start+batch_size]
            texts = batch[text_col].tolist()
            ids = batch[id_col].tolist() if has_id else batch["index"].tolist()

            batch_results = {id_col: ids, text_col: texts}

            for tok, mod, emo in zip(_tokenizers, _models, EMOTIONS):
                enc = tok(texts, padding=True, truncation=True, max_length=max_length, return_tensors="pt")
                enc = {k: v.to(_device) for k, v in enc.items()}
                out = mod(**enc)
                batch_results[emo] = out.logits.view(-1).tolist()

            all_chunks.append(pd.DataFrame(batch_results))

    return pd.concat(all_chunks, ignore_index=True)
