# Mixture of Cognitive Reasoners
## Modular Reasoning with Brain-Like Specialization

**Authors:** 1
EPFL

2
MIT

3
Harvard

### --- Section 0 ---

## Mixture of Cognitive Reasoners


## Modular Reasoning with Brain-Like Specialization


![ICLR](https://cognitive-reasoners.epfl.ch/images/iclr.png)


![Image](https://cognitive-reasoners.epfl.ch/images/hf-logo.png)


![Image](https://cognitive-reasoners.epfl.ch/images/hf-logo.png)

### --- Section 2 ---

## Abstract


Human cognitive behavior arises from the interaction of specialized brain networks dedicated to distinct functions, such as language, logic, and social reasoning. Inspired by this organization, we propose Mixture of Cognitive Reasoners (MiCRo): a modular, transformer-based architecture post-trained with a curriculum that induces functional specialization across experts. Concretely, we partition the layers of a pretrained language model into four expert modules aligned with well-studied cognitive networks in the human brain. MiCRo offers three key advantages over standard language models. (1) The specialized experts are interpretable and causally meaningful---ablating a module causes substantial drops on benchmarks requiring its specialized domain. (2) MiCRo's behavior can be dynamically steered at inference time by routing tokens to particular experts (e.g., favoring social over logical reasoning), enabling fine-grained control over outputs. (3) MiCRo outperforms or matches comparable baselines on both machine-learning reasoning benchmarks (e.g., GSM8K, BBH) and alignment to human behavior (CogBench), while maintaining interpretability. Taken together, cognitively grounded functional specialization yields models that are both more human-like and more human-interpretable.

### --- Section 3 ---

![The Human Language Network](https://cognitive-reasoners.epfl.ch/./images/preliminaries.png)


Fedorenko, E., Ivanova, A.A. & Regev, T.I. The language network as a natural kind within the broader landscape of the human brain. Nat. Rev. Neurosci. 25, 289-312 (2024).

### --- Section 4 ---

![The Human Language Network](https://cognitive-reasoners.epfl.ch/./images/training.png)

### --- Section 5 ---

Semantically Meaningful Routing Across Experts. 
              Token routing patterns in MiCRo-Llama-1B. Each bar indicates the proportion of tokens routed to a given expert across layers, with variance shown across sentences (n=50). The model exhibits clear domain-specific specialization consistent with the intended brain-inspired organization. For example, social cognition samples are routed to the social expert, while arithmetic tasks are routed to the logic expert. We find that the language expert is consistently activated in the early layers (see Appendix B for layer-wise routing plots and results from additional models). Two random samples are shown below each subplot.


![Token Routing Patterns Across Experts and Layers](https://cognitive-reasoners.epfl.ch/./images/token-routing.png)


Expert Ablations Reveal the Causal Contributions of Specialized modules.
              Top and bottom panels show results for MiCRo-Llama-1B and MiCRo-Llama-3B. Removing the Logic expert causes large drops on MATH and GSM8K, while removing the Social expert yields slight gains. For MMLU and BBH, results indicate that some group of subtasks rely on distinct experts, whereas others draw on overlapping contributions. Additional models in Appendix D.


![Steering Model Behavior via Expert Ablation](https://cognitive-reasoners.epfl.ch/./images/expert-ablations.png)


Neuroscience Localizers Recover Functionally Specialized Experts.
              (a) MiCRo-Llama-1B and (b) MiCRo-Llama-3B. For each model, we apply three neuroscience-inspired localizers—Language, Multiple Demand (MD) and Theory of Mind (ToM)—to examine the selectivity of localized units across experts and layers. Each plot shows the percentage of units in each expert of each layer that belongs to the top-10% selective units in the whole model.


![Neuroscience Localizers Identify Functionally Specialized Experts](https://cognitive-reasoners.epfl.ch/./images/localization.png)


Alignment with Human Behavior on CogBench.
(a) Average similarity score (SBRE) across 10 behavioral metrics, showing that MiCRo-Llama models achieves superior alignment compared to their MoB and Dense baselines. 
              (b) Human-normalized scores for each metric separately across the three models. 
              (c) Example inputs from two of the seven classical psychological experiments verbalized for LLM evaluation following CogBench.


![Alignment with Human Behavior on CogBench](https://cognitive-reasoners.epfl.ch/./images/behavioral-alignment.png)


Competitive Performance on Reasoning Benchmarks.
                Results on GSM8K (0-shot CoT), Minerva-Math, MMLU, and BBH (fewshot CoT). 
                MiCRo matches or outperforms baselines, and ablating the least relevant expert (e.g., social for math benchmarks) yields further gains. 
                For MoB (Ablation) and MiCRo (Ablation) (on MMLU and BBH subtasks), results reflect the best performance obtained when ablating up to one expert. 
                Significance is assessed with pairwise Welch's t-tests (shown in plot). 
                The dense model is shown as a dashed line. 
                Results of the remaining models and on more benchmarks are provided in Appendix E.


![Alignment with Human Behavior on CogBench](https://cognitive-reasoners.epfl.ch/./images/performance.png)

### --- Section 6 ---

## BibTeX


```
@inproceedings{alkhamissi2026micro,
            title={Mixture of Cognitive Reasoners: Modular Reasoning with Brain-Like Specialization},
            author={Badr AlKhamissi and C. Nicol{\`o} De Sabbata and Greta Tuckute and Zeming Chen and Martin Schrimpf and Antoine Bosselut},
            booktitle={The Fourteenth International Conference on Learning Representations},
            year={2026},
            url={https://openreview.net/forum?id=m3jztlHDmG}
        }
```

### --- Section 7 ---

## Acknowledgement


This website is adapted from LLaVA-VL and Nerfies, licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
