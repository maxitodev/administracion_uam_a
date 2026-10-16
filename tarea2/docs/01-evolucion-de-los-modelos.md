# 1. Evolución de los modelos

[← Volver al README](../README.md#parte-2-mcp-investigación)

## Qué es un modelo de lenguaje

Un modelo de lenguaje es un programa que, dado un texto, calcula qué tan probable es cada palabra (o pedazo de palabra, un *token*) que podría seguir. Con esa misma probabilidad puede calificar una oración completa: multiplica la probabilidad de cada palabra dadas las anteriores, lo que se conoce como regla de la cadena (Jurafsky & Martin, 2026). Generar texto es aplicar eso una y otra vez: elegir un token, agregarlo al texto y volver a predecir.

Los primeros modelos eran de *n-gramas*: contaban en un corpus cuántas veces aparecía cada secuencia corta de palabras. El problema es que casi ninguna oración nueva aparece tal cual en el corpus. Bengio et al. (2003) lo resolvieron con una red neuronal que aprende, al mismo tiempo, un vector para cada palabra (lo que hoy se llama *embedding*) y la función de probabilidad. Así, una oración vista en el entrenamiento también le enseña algo sobre oraciones parecidas que nunca vio.

## Cómo llegó a ser un modelo grande (LLM)

| Año | Paso | Qué cambió |
|---|---|---|
| 2003 | Modelo neuronal de Bengio et al. | Las palabras se representan como vectores aprendidos, no como conteos. |
| 2017 | Transformer (Vaswani et al.) | La atención reemplaza a la recurrencia: el entrenamiento se paraleliza y se puede usar mucho más texto. |
| 2018 | GPT (Radford et al.) | Se preentrena un modelo con texto sin etiquetar y después se ajusta a cada tarea. |
| 2019 | GPT-2, 1,500 millones de parámetros | Sin ajuste por tarea ya resuelve algunas tareas (*zero-shot*), y mejora conforme crece (Radford et al., 2019). |
| 2020 | GPT-3, 175,000 millones de parámetros | La tarea se explica con ejemplos dentro del mismo texto, sin reentrenar: aprendizaje en contexto (Brown et al., 2020). |
| 2020–2022 | Leyes de escalamiento | El error baja de forma predecible al crecer los parámetros, los datos y el cómputo (Kaplan et al., 2020). Chinchilla, de 70,000 millones, supera a modelos de 280,000 millones entrenándose con más datos (Hoffmann et al., 2022). |
| 2022 | InstructGPT (Ouyang et al.) | Con ajuste supervisado y retroalimentación humana (RLHF), un modelo de 1,300 millones de parámetros fue preferido sobre GPT-3 de 175,000 millones. |

Un LLM (*large language model*) es, entonces, el mismo modelo de lenguaje de siempre, sólo que basado en Transformer y entrenado con miles de millones de parámetros, una cantidad enorme de texto y mucho cómputo. «Grande» se refiere a las tres cosas, no sólo al número de parámetros.

Se habló mucho de *habilidades emergentes*: capacidades que no aparecen en modelos pequeños y de pronto sí en los grandes (Wei, Tay et al., 2022). Schaeffer et al. (2023) mostraron que buena parte de esos saltos dependen de la métrica que se usa para medir: con una métrica continua, la mejora es gradual. Es decir, crecer ayuda, pero no explica por sí solo todo lo que hoy hacen los modelos.

## Modelos con razonamiento explícito

Un modelo con razonamiento explícito escribe pasos intermedios antes de dar la respuesta: plantea el problema, prueba un camino, lo revisa y corrige. Esa capacidad no aparece sólo por hacer más grande el modelo. Viene de dos cosas que se agregan encima del preentrenamiento.

**1. Técnicas de entrenamiento y de uso.**

- *Cadena de pensamiento.* Si en el prompt se dan ejemplos resueltos paso a paso, el modelo imita los pasos y acierta más en problemas de aritmética y lógica (Wei, Wang et al., 2022). Incluso sin ejemplos, agregar «pensemos paso a paso» subió el acierto en el conjunto MultiArith de 17.7 % a 78.7 % con el mismo modelo (Kojima et al., 2022). La red es la misma; sólo cambió cómo se usa.
- *Aprendizaje por refuerzo.* Los modelos de razonamiento actuales se entrenan para producir esa cadena por su cuenta, premiando las respuestas que se pueden verificar, como un resultado matemático o un programa que pasa sus pruebas. OpenAI (2024) reportó que o1 mejora tanto con más entrenamiento por refuerzo como con más tiempo para pensar. DeepSeek-R1 mostró que el refuerzo puro, sin ejemplos de razonamiento escritos por personas, hace aparecer conductas como revisar y corregir la propia respuesta, y que eso se puede destilar a modelos más pequeños (Guo et al., 2025).

**2. Cómputo adicional al responder** (*test-time compute*). Pensar más cuesta más tokens y más tiempo. Snell et al. (2025) encontraron que repartir bien ese cómputo según la dificultad de la pregunta puede rendir más que usar un modelo 14 veces más grande. Por eso los proveedores lo ofrecen como un modo con presupuesto: Anthropic lo llama *extended thinking* y deja fijar cuántos tokens puede usar el modelo para razonar (Anthropic, s. f.-b); Google controla la profundidad con un nivel de *thinking* (Google, 2026).

El propio artículo de cadena de pensamiento advierte que la técnica funciona en modelos suficientemente grandes (Wei, Wang et al., 2022). Lo correcto es decir que el tamaño es necesario pero no suficiente: el razonamiento sale del entrenamiento y del cómputo extra al responder, no del tamaño solo.

## En resumen

- Un modelo de lenguaje predice el siguiente token; un LLM es ese mismo modelo llevado a gran escala con el Transformer.
- Escalar mejora el modelo de forma predecible, pero seguir instrucciones (RLHF) y razonar (cadena de pensamiento, refuerzo, cómputo al responder) se logran con técnicas que se agregan después.
- Aun así, el modelo sólo recibe texto y devuelve texto. Qué tan lejos llega con eso es el tema del [punto 2](02-el-problema-del-aislamiento.md).

## Referencias

Anthropic. (s. f.-b). *Extended thinking*. Claude Platform Docs. Recuperado el 15 de octubre de 2026, de https://platform.claude.com/docs/en/build-with-claude/extended-thinking

Bengio, Y., Ducharme, R., Vincent, P., & Jauvin, C. (2003). A neural probabilistic language model. *Journal of Machine Learning Research, 3*, 1137–1155. https://www.jmlr.org/papers/v3/bengio03a.html

Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., Agarwal, S., Herbert-Voss, A., Krueger, G., Henighan, T., Child, R., Ramesh, A., Ziegler, D., Wu, J., Winter, C., … Amodei, D. (2020). Language models are few-shot learners. *Advances in Neural Information Processing Systems, 33*, 1877–1901. https://proceedings.neurips.cc/paper/2020/hash/1457c0d6bfcb4967418bfb8ac142f64a-Abstract.html

Google. (2026, 14 de octubre). *Gemini thinking*. Gemini API, Google AI for Developers. https://ai.google.dev/gemini-api/docs/thinking

Guo, D., Yang, D., Zhang, H., Song, J., Wang, P., Zhu, Q., Xu, R., Zhang, R., Ma, S., Bi, X., Zhang, X., Yu, X., Wu, Y., Wu, Z. F., Gou, Z., Shao, Z., Li, Z., Gao, Z., Liu, A., … Zhang, Z. (2025). DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning. *Nature, 645*(8081), 633–638. https://doi.org/10.1038/s41586-025-09422-z

Hoffmann, J., Borgeaud, S., Mensch, A., Buchatskaya, E., Cai, T., Rutherford, E., de Las Casas, D., Hendricks, L. A., Welbl, J., Clark, A., Hennigan, T., Noland, E., Millican, K., van den Driessche, G., Damoc, B., Guy, A., Osindero, S., Simonyan, K., Elsen, E., … Sifre, L. (2022). *Training compute-optimal large language models* [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2203.15556

Jurafsky, D., & Martin, J. H. (2026). *Speech and language processing: An introduction to natural language processing, computational linguistics, and speech recognition with language models* (3.ª ed., borrador en línea del 19 de agosto de 2026). https://web.stanford.edu/~jurafsky/slp3/

Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B., Chess, B., Child, R., Gray, S., Radford, A., Wu, J., & Amodei, D. (2020). *Scaling laws for neural language models* [Preprint]. arXiv. https://doi.org/10.48550/arXiv.2001.08361

Kojima, T., Gu, S. S., Reid, M., Matsuo, Y., & Iwasawa, Y. (2022). Large language models are zero-shot reasoners. *Advances in Neural Information Processing Systems, 35*, 22199–22213. https://doi.org/10.52202/068431-1613

OpenAI. (2024, 12 de septiembre). *Learning to reason with LLMs*. https://openai.com/index/learning-to-reason-with-llms/

Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C., Mishkin, P., Zhang, C., Agarwal, S., Slama, K., Ray, A., Schulman, J., Hilton, J., Kelton, F., Miller, L., Simens, M., Askell, A., Welinder, P., Christiano, P. F., Leike, J., & Lowe, R. (2022). Training language models to follow instructions with human feedback. *Advances in Neural Information Processing Systems, 35*, 27730–27744. https://doi.org/10.52202/068431-2011

Radford, A., Narasimhan, K., Salimans, T., & Sutskever, I. (2018). *Improving language understanding by generative pre-training* [Informe técnico]. OpenAI. https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf

Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., & Sutskever, I. (2019). *Language models are unsupervised multitask learners* [Informe técnico]. OpenAI. https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf

Schaeffer, R., Miranda, B., & Koyejo, S. (2023). Are emergent abilities of large language models a mirage? *Advances in Neural Information Processing Systems, 36*, 55565–55581. https://doi.org/10.52202/075280-2425

Snell, C., Lee, J., Xu, K., & Kumar, A. (2025). Scaling LLM test-time compute optimally can be more effective than scaling parameters for reasoning. En *International Conference on Learning Representations* (Vol. 2025, pp. 10131–10165). https://proceedings.iclr.cc/paper_files/paper/2025/hash/1b623663fd9b874366f3ce019fdfdd44-Abstract-Conference.html

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., & Polosukhin, I. (2017). Attention is all you need. *Advances in Neural Information Processing Systems, 30*. https://proceedings.neurips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html

Wei, J., Tay, Y., Bommasani, R., Raffel, C., Zoph, B., Borgeaud, S., Yogatama, D., Bosma, M., Zhou, D., Metzler, D., Chi, E. H., Hashimoto, T., Vinyals, O., Liang, P., Dean, J., & Fedus, W. (2022). Emergent abilities of large language models. *Transactions on Machine Learning Research*. https://openreview.net/forum?id=yzkSU5zdwD

Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q. V., & Zhou, D. (2022). Chain-of-thought prompting elicits reasoning in large language models. *Advances in Neural Information Processing Systems, 35*, 24824–24837. https://doi.org/10.52202/068431-1800
