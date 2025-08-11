import asyncio
from agents import synth


def test_synthesize_model_choice(monkeypatch):
    docs = [{"title": "t", "url": "u", "text": "x"}]

    async def fake_generate(prompt, model, task_tokens):
        return model

    monkeypatch.setattr(synth, "generate", fake_generate)
    res_small = asyncio.run(synth.synthesize("q", docs, 500))
    res_big = asyncio.run(synth.synthesize("q", docs, 1300))
    assert res_small == synth.DEFAULT_SMALL
    assert res_big == synth.DEFAULT_BIG
