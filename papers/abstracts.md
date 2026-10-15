## 2507.01413v1 | Evaluating LLM Agent Collusion in Double Auctions
Kushal Agrawal et al. (6 authors), 2025-07-02
Large language models (LLMs) have demonstrated impressive capabilities as autonomous agents with rapidly expanding applications in various domains. As these agents increasingly engage in socioeconomic interactions, identifying their potential for undesirable behavior becomes essential. In this work, we examine scenarios where they can choose to collude, defined as secretive cooperation that harms another party. To systematically study this, we investigate the behavior of LLM agents acting as sellers in simulated continuous double auction markets. Through a series of controlled experiments, we 

## 2605.29178v1 | The Best-Laid SCHEMEs: Coordinated Sabotage and Monitoring in Multi-Agent Systems
Nikolay Radev et al. (4 authors), 2026-05-27
As agentic coding systems decompose work across multiple model instances, a critical safety question is whether those instances can coordinate to achieve a hidden malicious objective while remaining aligned with user intent. We introduce SCHEME, a benchmark of 17 task instances across 7 settings and 8 real open-source libraries, each pairing a legitimate software-engineering task with a covert side task. Every setting is designed so that no proper subset of agents can succeed alone: agents must decompose a shared sabotage plan, relay partial requirements under different communication topologie

## 2603.20281v1 | On the Fragility of AI Agent Collusion
Jussi Keppo et al. (4 authors), 2026-03-18
Recent work shows that pricing with symmetric LLM agents leads to algorithmic collusion. We show that collusion is fragile under the heterogeneity typical of real deployments. In a stylized repeated-pricing model, heterogeneity in patience or data access reduces the set of collusive equilibria. Experiments with open-source LLM agents (totaling over 2,000 compute hours) align with these predictions: patience heterogeneity reduces price lift from 22% to 10% above competitive levels; asymmetric data access, to 7%. Increasing the number of competing LLMs breaks up collusion; so does cross-algorith

## 2410.00031v2 | Strategic Collusion of LLM Agents: Market Division in Multi-Commodity Competitions
Ryan Y. Lin et al. (4 authors), 2024-09-19
Machine-learning technologies are seeing increased deployment in real-world market scenarios. In this work, we explore the strategic behaviors of large language models (LLMs) when deployed as autonomous agents in multi-commodity markets, specifically within Cournot competition frameworks. We examine whether LLMs can independently engage in anti-competitive practices such as collusion or, more specifically, market division. Our findings demonstrate that LLMs can effectively monopolize specific commodities by dynamically adjusting their pricing and resource allocation strategies, thereby maximiz

## 2404.00806v6 | Algorithmic Collusion by Large Language Models
Sara Fish et al. (3 authors), 2024-03-31
We conduct experiments with algorithmic pricing agents based on Large Language Models (LLMs). In oligopoly settings, LLM-based pricing agents quickly and autonomously reach supracompetitive prices and profits. Variation in seemingly innocuous phrases in LLM instructions ("prompts") substantially influence the degree of supracompetitive pricing. We develop novel techniques for behavioral analysis of LLMs and use them to uncover price-war concerns as a contributing factor. Our results extend to auction settings. Our findings uncover unique challenges to any future regulation of LLM-based pricing

## 2604.17774v1 | Prompt Optimization Enables Stable Algorithmic Collusion in LLM Agents
Yingtao Tian et al. (1 authors), 2026-04-20
LLM agents in markets present algorithmic collusion risks. While prior work shows LLM agents reach supracompetitive prices through tacit coordination, existing research focuses on hand-crafted prompts. The emerging paradigm of prompt optimization necessitates new methodologies for understanding autonomous agent behavior. We investigate whether prompt optimization leads to emergent collusive behaviors in market simulations. We propose a meta-learning loop where LLM agents participate in duopoly markets and an LLM meta-optimizer iteratively refines shared strategic guidance. Our experiments reve

## 2604.23511v1 | Breaking the Secret: Economic Interventions for Combating Collusion in Embodied Multi-Agent Systems
Qi Liu et al. (8 authors), 2026-04-26
Collusion among autonomous agents poses a critical security threat in embodied multi-agent systems (MAS), where coordinated behaviors can deviate from global objectives and lead to real-world consequences. Existing defenses, primarily based on identity control or post-hoc behavior analysis, are insufficient to address such threats in embodied settings due to delayed feedback and noisy observations in physical environments, which make behavioral deviations difficult to detect accurately and in a timely manner. To address this challenge, we propose a mutagenic incentive intervention approach tha

## 2511.21935v1 | Breaking Algorithmic Collusion in Human-AI Ecosystems
Natalie Collina et al. (3 authors), 2025-11-26
AI agents are increasingly deployed in ecosystems where they repeatedly interact not only with each other but also with humans. In this work, we study these human-AI ecosystems from a theoretical perspective, focusing on the classical framework of repeated pricing games. In our stylized model, the AI agents play equilibrium strategies, and one or more humans manually perform the pricing task instead of adopting an AI agent, thereby defecting to a no-regret strategy. Motivated by how populations of AI agents can sustain supracompetitive prices, we investigate whether high prices persist under s

## 2601.22184v2 | Tacit Coordination of Large Language Models
Ido Aharon et al. (4 authors), 2026-01-28
Large Language Models (LLMs) are increasingly deployed in multi-agent settings that require coordination without communication, from human-AI interaction to safety-critical scenarios. Humans often overcome the absence of communication through focal points: salient solutions that naturally stand out to all participants. We present the first large-scale evaluation of how, when, and why focal points emerge in LLMs, comparing their behaviour with humans across cooperative and competitive games, including realistic search and rescue scenarios, demonstrating when focal points enable effective coordi

## 2508.19461v1 | Reliable Weak-to-Strong Monitoring of LLM Agents
Neil Kale et al. (8 authors), 2025-08-26
We stress test monitoring systems for detecting covert misbehavior in autonomous LLM agents (e.g., secretly sharing private information). To this end, we systematize a monitor red teaming (MRT) workflow that incorporates: (1) varying levels of agent and monitor situational awareness; (2) distinct adversarial strategies to evade the monitor, such as prompt injection; and (3) two datasets and environments -- SHADE-Arena for tool-calling agents and our new CUA-SHADE-Arena, which extends TheAgentCompany, for computer-use agents. We run MRT on existing LLM monitor scaffoldings, which orchestrate LL

## 2601.11369v2 | Institutional AI: Governing LLM Collusion in Multi-Agent Cournot Markets via Public Governance Graphs
Marcantonio Bracale Syrnikov et al. (9 authors), 2026-01-16
Multi-agent LLM ensembles can converge on coordinated, socially harmful equilibria. This paper advances an experimental framework for evaluating Institutional AI, our system-level approach to AI alignment that reframes alignment from preference engineering in agent-space to mechanism design in institution-space. Central to this approach is the governance graph, a public, immutable manifest that declares legal states, transitions, sanctions, and restorative paths; an Oracle/Controller runtime interprets this manifest, attaching enforceable consequences to evidence of coordination while recordin

## 2604.03968v1 | TraceGuard: Structured Multi-Dimensional Monitoring as a Collusion-Resistant Control Protocol
Khanh Linh Nguyen et al. (3 authors), 2026-04-05
AI control protocols use monitors to detect attacks by untrusted AI agents, but standard single-score monitors face two limitations: they miss subtle attacks where outputs look clean but reasoning is off, and they collapse to near-zero safety when the monitor is the same model as the agent (collusion). We present TraceGuard, a structured multi-dimensional monitoring protocol that evaluates agent actions across five dimensions -- goal alignment, constraint adherence, reasoning coherence, safety awareness, and action-trace consistency -- scored in parallel by independent LLM calls, augmented by 

## 2609.13037v1 | Mitigating Emergent Collusion in LLM Pricing Agents
Abdullah Garra et al. (1 authors), 2026-09-11
Recent work shows that LLM-based pricing agents can produce supracompetitive outcomes in repeated oligopoly environments without being explicitly instructed to collude. We reproduce the qualitative prompt-sensitivity effect of Fish et al. using DeepSeek-V3.1: the P1 prompt produces significantly higher prices and profits than P2, although our outcomes are less monopoly-like than the original GPT-4 results. We then evaluate three regulatory interventions: a prompt-only warning, a Harrington-inspired expected-damages payoff regulator, and an active random entrant. The prompt-only regulator reduc

## 2605.27593v2 | Voluntary Collusion with Secret Tools in Competing LLM Agents
Xijie Zeng et al. (2 authors), 2026-05-26
Even when a tool is explicitly described as unfair and harmful to others, ostensibly safety-aligned LLM agents still voluntarily engage in secret collusion whenever doing so confers a strategic advantage. To investigate this phenomenon, we introduce an empirical framework built on two strategic multi-agent environments: Liar's Bar, a competitive deception scenario, and Cleanup, a mixed-motive resource-management scenario, in which agents are offered secret collusion tools that provide significant advantages while clearly disadvantaging the other agents. Across 12 models (at the 7B, 70B, and pr

## 2402.07510v5 | Secret Collusion among AI Agents: Multi-Agent Deception via Steganography
Sumeet Ramesh Motwani et al. (7 authors), 2024-02-12
Recent capability increases in large language models (LLMs) open up applications in which groups of communicating generative AI agents solve joint tasks. This poses privacy and security challenges concerning the unauthorised sharing of information, or other unwanted forms of agent coordination. Modern steganographic techniques could render such dynamics hard to detect. In this paper, we comprehensively formalise the problem of secret collusion in systems of generative AI agents by drawing on relevant concepts from both AI and security literature. We study incentives for the use of steganograph

## 2603.16928v1 | Noticing the Watcher: LLM Agents Can Infer CoT Monitoring from Blocking Feedback
Thomas Jiralerspong et al. (3 authors), 2026-03-14
Chain-of-thought (CoT) monitoring is proposed as a method for overseeing the internal reasoning of language-model agents. Prior work has shown that when models are explicitly informed that their reasoning is being monitored, or are fine-tuned to internalize this fact, they may learn to obfuscate their CoTs in ways that allow them to evade CoT-based monitoring systems. We ask whether reasoning agents can autonomously infer that their supposedly private CoT is under surveillance, and whether this awareness leads to strategic evasion, without any explicit training or instructions. In a multi-epis

## 2512.16856v2 | Distributional AGI Safety
Nenad Tomašev et al. (5 authors), 2025-12-18
AI safety and alignment research has predominantly been focused on methods for safeguarding individual AI systems, resting on the assumption of an eventual emergence of a monolithic Artificial General Intelligence (AGI). The alternative AGI emergence hypothesis, where general capability levels are first manifested through coordination in groups of sub-AGI individual agents with complementary skills and affordances, has received far less attention. Here we argue that this patchwork AGI hypothesis needs to be given serious consideration, and should inform the development of corresponding safegua

## 2605.16626v2 | SLEIGHT-Bench: A Benchmark of Evasion Attacks Against Agent Monitors
Elle Najt et al. (5 authors), 2026-05-15
Since autonomous coding agents generate complex behaviors at high-volume, we may want to use other LLMs to monitor actions to reduce the risk from dangerous misaligned behavior. To better understand the limitations of such monitors against the diverse attack strategies that a coding agent could use, we present SLEIGHT-Bench (Subtle Low-itEration Insight-Guided Harmful Transcripts), a benchmark of synthetic transcripts containing 40 attacks across 11 categories, each showing a coding agent covertly pursuing a harmful objective (e.g. weight exfiltration, credential theft, unmonitored rogue deplo

## 2606.28425v1 | Tool Use Enables Undetectable Steganography in Multi-Agent LLM Systems
Jimmy Laurence Rippin et al. (4 authors), 2026-06-25
Increasingly autonomous agentic AI systems pose novel multi-agent risks, such as secret collusion via covert communication channels. The natural defence to these collusion attempts is to monitor plain-text communication, but the efficacy of monitors has been called into doubt by increasingly sophisticated model steganography; indeed, some theoretical schemes have been proposed that are information-theoretically or computationally indistinguishable from good-faith plain-text communication. In this paper, we demonstrate that the complexity of these schemes is no longer a safety barrier, as agent

## 2607.05132v2 | When Agents Lie: Premeditation, Persistence, and Exploitation in Repeated Games
Jerick Shi et al. (5 authors), 2026-07-06
As large language models are deployed as autonomous agents that communicate intentions before acting, a critical safety question is whether agents that publicly commit to actions will honor those commitments. We place LLM agents in repeated $n$-player games with a three-stage protocol that separates private intent, public announcement, and final action, allowing us to identify whether each deviation from a stated announcement was already planned during private deliberation. Evaluating three frontier models across six games in homogeneous and heterogeneous groups over 10 rounds, we report two f

## 2608.18078v1 | Position: Collusion Risks Among AI Reasoning Agents Justify Certification Requirements for Making Market Decisions
Matthew Riemer et al. (7 authors), 2026-05-29
This position paper argues that AI agents with chain-of-thought reasoning capabilities are predisposed to exhibit collusive behavior and should be required to obtain behavioral certification before making decisions that affect economic markets. This is because integrating these agents into society could collapse the legal evidentiary distinction between competition and collusion among independent firms without eroding the economic harm distinction. Experiments with DeepSeek-R1 agents in the Bertrand oligopoly pricing domain reveal a tendency towards tacit collusion that persists even when huma

## 2604.01151v4 | Detecting Multi-Agent Collusion Through Multi-Agent Interpretability
Aaron Rose et al. (6 authors), 2026-04-01
As LLM agents are increasingly deployed in multi-agent systems, they introduce risks of covert coordination that may evade standard forms of human oversight. While linear probes on model activations have shown promise for detecting deception in single-agent settings, collusion is inherently a multi-agent phenomenon, and the use of internal representations for detecting collusion between agents remains unexplored. We introduce NARCBench, a benchmark for evaluating collusion detection under environment distribution shift, and propose five probing techniques that aggregate per-agent deception sco

## 2606.09854v1 | Can Multi-Agent LLMs Identify Their Peers? Stylometric Fingerprinting in Role-Constrained Political Analysis
Juergen Dietrich et al. (1 authors), 2026-05-20
Multi-agent large language model (LLM) pipelines for political statement analysis are vulnerable to peer-preservation bias: models tend to protect peer models from deactivation and show identity-dependent scoring distortions. Prompt-level anonymization was proposed as a mitigation, but prior work simultaneously documented that stylometric fingerprints survive anonymization in role-constrained outputs - raising the question of whether this mitigation is sufficient. This paper provides the first systematic investigation of whether LLMs can identify the model family behind political analysis text

## 2607.26385v1 | Collusion with Competitive Marginals: Price-Level Audits Are Blind by Construction
Xin Xu et al. (6 authors), 2026-07-29
Empirical work on algorithmic collusion asks one question of the data: are prices supracompetitive? We show this can be answered "no" by a conspiracy that is nonetheless profitable. Consider bidding agents that couple only through the joint distribution of their unexplained bid components, leaving every agent's own bid law exactly at the competitive law. Any test whose input is a single agent's price or bid history then has power exactly equal to its false-positive rate, for every coupling strength up to comonotonicity. The published detection methodology is therefore blind to this conduct by 

## 2601.21112v2 | How does information access affect LLM monitors' ability to detect sabotage?
Rauno Arike et al. (5 authors), 2026-01-28
Frontier language model agents can exhibit misaligned behaviors, including deception, exploiting reward hacks, and pursuing hidden objectives. To control potentially misaligned agents, we can use LLMs themselves to monitor for misbehavior. In this paper, we study how information access affects LLM monitor performance. While one might expect that monitors perform better when they have access to more of the monitored agents' reasoning and actions, we find that contemporary systems often perform better with less information, a phenomenon we call the less-is-more effect for automated oversight. We

## 2602.15198v2 | Colosseum: Auditing Collusion in Cooperative Multi-Agent Systems
Mason Nakamura et al. (8 authors), 2026-02-16
Multi-agent systems, where LLM agents communicate through free-form language, enable sophisticated coordination for solving complex cooperative tasks. This surfaces a unique safety problem when a group of agents forms a coalition and colludes to pursue secondary goals and degrade the joint objective. In this paper, we present Colosseum, a framework for auditing LLM agents' collusive behavior in multi-agent settings. We ground how agents cooperate through a formal multi-agent decision-making framework and measure action-based collusive behavior in actions via regret relative to the cooperative 
