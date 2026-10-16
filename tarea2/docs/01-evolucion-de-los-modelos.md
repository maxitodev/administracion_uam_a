# 1. Evolución de los modelos

[← Volver al README](../README.md#parte-2-mcp-investigación)

Un modelo de lenguaje calcula qué tan probable es cada palabra (o *token*) que puede seguir a un texto. Para generar, elige un token, lo agrega y vuelve a predecir (Jurafsky & Martin, 2026). Los primeros modelos contaban secuencias de palabras en un corpus. Bengio et al. (2003) usaron una red neuronal que aprende un vector por palabra, así una oración vista en el entrenamiento le enseña algo sobre otras parecidas.

## De modelo de lenguaje a LLM

| Año | Qué cambió |
|---|---|
| 2017 | El Transformer cambia la recurrencia por atención y permite entrenar en paralelo con mucho más texto (Vaswani et al., 2017). |
| 2020 | GPT-3, con 175 mil millones de parámetros, resuelve tareas con sólo ver ejemplos en el prompt (Brown et al., 2020). |
| 2020 | El error baja de forma predecible al aumentar parámetros, datos y cómputo (Kaplan et al., 2020). |
| 2022 | Con retroalimentación humana (RLHF), las personas prefirieron un modelo de 1,300 millones de parámetros sobre GPT-3 (Ouyang et al., 2022). |

Un LLM es el mismo modelo de lenguaje a gran escala: miles de millones de parámetros, enormes cantidades de texto y mucho cómputo. La última fila ya muestra que el tamaño no lo explica todo.

## Modelos con razonamiento explícito

Son modelos que escriben pasos intermedios antes de responder y revisan su propio camino. Esa capacidad no aparece sólo por hacer más grande el modelo:

- **Técnicas de entrenamiento.** Pedirle que razone paso a paso mejora sus respuestas en matemáticas y lógica (Kojima et al., 2022; Wei et al., 2022). Los modelos actuales se entrenan con aprendizaje por refuerzo para hacerlo por su cuenta, premiando respuestas que se pueden verificar (Guo et al., 2025; OpenAI, 2024).
- **Cómputo adicional al responder.** Pensar más cuesta más tokens y más tiempo, pero rinde: repartir bien ese cómputo puede superar a un modelo 14 veces más grande (Snell et al., 2025).

El tamaño ayuda, pero el razonamiento viene del entrenamiento y del cómputo extra. Aun así, el modelo sigue recibiendo texto y devolviendo texto ([punto 2](02-el-problema-del-aislamiento.md)).

## Referencias

Bengio, Y., Ducharme, R., Vincent, P., & Jauvin, C. (2003). A neural probabilistic language model. *Journal of Machine Learning Research, 3*, 1137–1155. https://www.jmlr.org/papers/v3/bengio03a.html

Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., Agarwal, S., Herbert-Voss, A., Krueger, G., Henighan, T., Child, R., Ramesh, A., Ziegler, D., Wu, J., Winter, C., … Amodei, D. (2020). Language models are few-shot learners. *Advances in Neural Information Processing Systems, 33*, 1877–1901. https://proceedings.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html

Guo, D., Yang, D., Zhang, H., Song, J., Wang, P., Zhu, Q., Xu, R., Zhang, R., Ma, S., Bi, X., Zhang, X., Yu, X., Wu, Y., Wu, Z. F., Gou, Z., Shao, Z., Li, Z., Gao, Z., Liu, A., … Zhang, Z. (2025). DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning. *Nature, 645*(8081), 633–638. https://doi.org/10.1038/s41586-025-09422-z

Jurafsky, D., & Martin, J. H. (2026). *Speech and language processing* (3.ª ed., borrador en línea del 19 de agosto de 2026). https://web.stanford.edu/~jurafsky/slp3/

Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B., Chess, B., Child, R., Gray, S., Radford, A., Wu, J., & Amodei, D. (2020). *Scaling laws for neural language models* [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2001.08361

Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., & Iwasawa, Y. (2022). Large language models are zero-shot reasoners. *Advances in Neural Information Processing Systems, 35*, 22199–22213. https://doi.org/10.52202/068431-1613

OpenAI. (2024, 12 de septiembre). *Learning to reason with LLMs*. https://openai.com/index/learning-to-reason-with-llms/

Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C., Mishkin, P., Zhang, C., Agarwal, S., Slama, K., Ray, A., Schulman, J., Hilton, J., Kelton, F., Miller, L., Simens, M., Askell, A., Welinder, P., Christiano, P. F., Leike, J., & Lowe, R. (2022). Training language models to follow instructions with human feedback. *Advances in Neural Information Processing Systems, 35*, 27730–27744. https://doi.org/10.52202/068431-2011

Snell, C., Lee, J., Xu, K., & Kumar, A. (2025). Scaling LLM test-time compute optimally can be more effective than scaling parameters for reasoning. En *International Conference on Learning Representations* (Vol. 2025, pp. 10131–10165). https://proceedings.iclr.cc/paper_files/paper/2025/hash/1b623663fd9b874366f3ce019fdfdd44-Abstract-Conference.html

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems, 30*. https://proceedings.neurips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html

Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q. V., & Zhou, D. (2022). Chain-of-thought prompting elicits reasoning in large language models. *Advances in Neural Information Processing Systems, 35*, 24824–24837. https://doi.org/10.52202/068431-1800
