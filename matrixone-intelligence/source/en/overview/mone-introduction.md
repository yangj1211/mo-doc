Built on MatrixOne's native vector capabilities, we've launched **MOne**, an AI-powered document Q&A assistant. From the cloud platform you can ask MOne questions in natural language and get the MatrixOne information you need — no manual digging through docs — for a much smoother, more personalized experience.

## How it works

The AI framework is LangChain. Embeddings come from the OpenAI Embedding model, and the LLM is GPT-3.5-Turbo. MatrixOne Intelligence calls the OpenAI embedding endpoint to produce a vector representation of each text chunk, stores those vectors and runs similarity search using MatrixOne's native vector capabilities, collects the top-matching chunks, and finally calls GPT-3.5 to refine and generate the answer.

The flow has two parts:

- Load file → read text → split into chunks → vectorize → store vectors in MatrixOne
- User asks a question → vectorize the question → match against stored vectors to find the most similar chunks → use the matched chunks as context alongside the question in the prompt → submit to the LLM to generate the answer

The end-to-end pipeline:

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/overview/mone-1.png width=70% heigth=70%/>
</div>

## How to use MOne

After logging in to the instance management console or the database management console, click the MOne icon in the bottom-right corner to wake it up.

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/overview/mone-2.png)

On the question page you can click any of the suggested questions to start the conversation directly, or type your own MatrixOne-related question. There's a one-click copy button as well — once you have the answer you want, click the copy icon in the bottom-right of the response. If MOne's answer was helpful, give it a thumbs-up.

:::{note}
MOne is built on an LLM. Because of inherent LLM limitations, the answer can occasionally miss the mark. MOne also only answers MatrixOne product-related questions, and your question can be at most 200 characters long.
:::
