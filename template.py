# -*- coding: utf-8 -*-
"""
这段代码定义了一个Conversation类和一个全局注册表conv_templates，用于管理语言模型的不同会话模板。下面是代码的细分:

Conversation类是一个包含以下字段的数据类:

name:对话模板的名称。
system_prompt:设置上下文的初始系统提示符。
messages:消息序列的列表，其中每个序列是一对[查询，回答]。
roles:说话者的角色，通常是“USER”、“ASSISTANT”。
提示:每个会话回合使用的提示格式。
sep:匝间使用的分隔字符串。
stop_str:文本生成的可选停止标记(默认为"</s>")。
该类提供了获取提示符(get_prompt)、获取完整对话框(get_dialog)和附加新消息(append_message)的方法。

register_conv_template函数用于在全局conv_templates字典中注册一个新的Conversation实例。

代码为不同的语言模型定义了几个预定义的会话模板，如Vicuna、Alpaca、baihuan、ChatGLM、Phoenix、BELLE、Aquila、Intern、StarChat、LLaMa2、LLaMa3、Chinese LLaMa2、Mistral、XVERSE、QWen、Deepseek、DeepseekCoder、Yi、Orion、Cohere和QWen(用于代码生成)。

get_conv_template函数根据提供的名称从conv_templates字典中检索特定的Conversation实例。

此代码可能用于与不同语言模型交互的大型系统中。通过定义和注册对话模板，系统可以轻松地为各种模型格式化提示并管理对话历史。这些模板处理不同的格式需求，例如演讲者角色、提示符、分隔符和停止令牌，从而更容易一致地使用多个模型。
"""

from dataclasses import dataclass
from typing import Optional, List, Dict, Sequence

__all__ = ['Conversation', 'register_conv_template', 'get_conv_template']


@dataclass
class Conversation:
    """A class that manages prompt templates and keeps all conversation history."""

    # The name of this template
    name: str
    # The system prompt
    system_prompt: str
    # All messages. format: list of [question, answer]
    messages: Optional[List[Sequence[str]]]
    # The roles of the speakers
    roles: Optional[Sequence[str]]
    # Conversation prompt
    prompt: str
    # Separator
    sep: str
    # Stop token, default is tokenizer.eos_token
    stop_str: Optional[str] = "</s>"

    def get_prompt(
            self,
            messages: Optional[List[Sequence[str]]] = None,
            system_prompt: Optional[str] = ""
    ) -> str:
        """
        Returns a string containing prompt without response.
        """
        return "".join(self._format_example(messages, system_prompt))

    def get_dialog(
            self,
            messages: Optional[List[Sequence[str]]] = None,
            system_prompt: Optional[str] = ""
    ) -> List[str]:
        """
        Returns a list containing 2 * n elements where the 2k-th is a query and the (2k+1)-th is a response.
        """
        return self._format_example(messages, system_prompt)

    def _format_example(
            self,
            messages: Optional[List[Sequence[str]]] = None,
            system_prompt: Optional[str] = ""
    ) -> List[str]:
        system_prompt = system_prompt or self.system_prompt
        system_prompt = system_prompt + self.sep if system_prompt else ""  # add separator for non-empty system prompt
        messages = messages or self.messages
        convs = []
        for turn_idx, [user_query, bot_resp] in enumerate(messages):
            if turn_idx == 0:
                convs.append(system_prompt + self.prompt.format(query=user_query))
                convs.append(bot_resp)
            else:
                convs.append(self.sep + self.prompt.format(query=user_query))
                convs.append(bot_resp)
        return convs

    def append_message(self, query: str, answer: str):
        """Append a new message."""
        self.messages.append([query, answer])


# A global registry for all conversation templates
conv_templates: Dict[str, Conversation] = {}


def register_conv_template(template: Conversation):
    """Register a new conversation template."""
    conv_templates[template.name] = template


"""Vicuna v1.1 template
Supports: https://huggingface.co/lmsys/vicuna-7b-delta-v1.1
          https://huggingface.co/lmsys/vicuna-13b-delta-v1.1
"""
register_conv_template(
    Conversation(
        name="vicuna",
        system_prompt="A chat between a curious user and an artificial intelligence assistant. "
                      "The assistant gives helpful, detailed, and polite answers to the user's questions.",
        messages=[],
        roles=("USER", "ASSISTANT"),
        prompt="USER: {query} ASSISTANT:",
        sep="</s>",
    )
)

"""Base model template, for few shot"""
register_conv_template(
    Conversation(
        name="base",
        system_prompt="",
        messages=[],
        roles=("USER", "ASSISTANT"),
        prompt="{query}",
        sep="</s>",
    )
)

"""Alpaca template"""
register_conv_template(
    Conversation(
        name="alpaca",
        system_prompt="Below is an instruction that describes a task. "
                      "Write a response that appropriately completes the request.",
        messages=[],
        roles=("### Instruction", "### Response"),
        prompt="### Instruction:\n{query}\n\n### Response:\n",
        sep="\n\n",
    )
)

"""Baichuan template
source: https://huggingface.co/baichuan-inc/Baichuan-13B-Chat/blob/main/generation_utils.py#L31
Support: https://huggingface.co/baichuan-inc/Baichuan-13B-Chat
"""
register_conv_template(
    Conversation(
        name="baichuan",
        system_prompt="",
        messages=[],
        roles=("<reserved_102>", "<reserved_103>"),
        prompt="<reserved_102>{query}<reserved_103>",
        sep="</s>",
    )
)

"""Baichuan2 template
Support: https://huggingface.co/baichuan-inc/Baichuan2-7B-Chat
         https://huggingface.co/baichuan-inc/Baichuan2-13B-Chat
"""
register_conv_template(
    Conversation(
        name="baichuan2",
        system_prompt="",
        messages=[],
        roles=("<reserved_106>", "<reserved_107>"),
        prompt="<reserved_106>{query}<reserved_107>",
        sep="</s>",
    )
)

"""ziya template"""
register_conv_template(
    Conversation(
        name="ziya",
        system_prompt="",
        messages=[],
        roles=("<human>", "<bot>"),
        prompt="<human>:{query}\n<bot>:",
        sep="\n",
    )
)

"""Linly template"""
register_conv_template(
    Conversation(
        name="linly",
        system_prompt="",
        messages=[],
        roles=("User", "Bot"),
        prompt="User: {query}\nBot: ",
        sep="\n",
    )
)

"""ChatGLM1 template
Support: https://huggingface.co/THUDM/chatglm-6b
source: https://huggingface.co/THUDM/chatglm-6b/blob/main/modeling_chatglm.py#L1307
"""
register_conv_template(
    Conversation(
        name="chatglm",
        system_prompt="",
        messages=[],
        roles=("问", "答"),
        prompt="问：{query}\n答：",
        sep="\n",
    )
)

"""ChatGLM2 template
Support: https://huggingface.co/THUDM/chatglm2-6b
source: https://huggingface.co/THUDM/chatglm2-6b/blob/main/modeling_chatglm.py#L1007
"""
register_conv_template(
    Conversation(
        name="chatglm2",
        system_prompt="",
        messages=[],
        roles=("问", "答"),
        prompt="问：{query}\n\n答：",
        sep="\n\n",
    )
)

"""ChatGLM3 template
Support: https://huggingface.co/THUDM/chatglm3-6b
source: https://huggingface.co/THUDM/chatglm3-6b/blob/main/tokenization_chatglm.py#L179
"""
register_conv_template(
    Conversation(
        name="chatglm3",
        system_prompt="",
        messages=[],
        roles=("<|user|>", "<|assistant|>"),
        prompt="<|user|>\n{query}<|assistant|>",
        sep="\n",
        stop_str="<|user|>",
    )
)

"""Phoenix template"""
register_conv_template(
    Conversation(
        name="phoenix",
        system_prompt="A chat between a curious human and an artificial intelligence assistant. "
                      "The assistant gives helpful, detailed, and polite answers to the human's questions.\n\n",
        messages=[],
        roles=("Human", "Assistant"),
        prompt="Human: <s>{query}</s>Assistant: ",
        sep="</s>",
    )
)

"""belle template
Supports: https://huggingface.co/BelleGroup/BELLE-LLaMA-EXT-13B
"""
register_conv_template(
    Conversation(
        name="belle",
        system_prompt="",
        messages=[],
        roles=("Human", "Belle"),
        prompt="Human: {query}\n\nBelle: ",
        sep="\n\n",
    )
)

"""aquila template
Supports: https://huggingface.co/qhduan/aquilachat-7b
          https://huggingface.co/BAAI/AquilaChat2-34B
"""
register_conv_template(
    Conversation(
        name="aquila",
        system_prompt="A chat between a curious human and an artificial intelligence assistant. "
                      "The assistant gives helpful, detailed, and polite answers to the human's questions.",
        messages=[],
        roles=("Human", "Assistant"),
        prompt="Human: {query}###Assistant:",
        sep="###",
    )
)

"""intern template
Supports: https://huggingface.co/internlm/internlm-chat-7b
          https://huggingface.co/internlm/internlm-chat-20b
"""
register_conv_template(
    Conversation(
        name="intern",
        system_prompt="",
        messages=[],
        roles=("<|User|>", "<|Bot|>"),
        prompt="<|User|>:{query}<eoh>\n<|Bot|>:",
        sep="<eoa>\n",
        stop_str="<eoa>",
    )
)

"""StarChat template
Supports: https://huggingface.co/HuggingFaceH4/starchat-alpha
          https://huggingface.co/HuggingFaceH4/starchat-beta
"""
register_conv_template(
    Conversation(
        name="starchat",
        system_prompt="<system>\n",
        messages=[],
        roles=("<|user|>", "<|assistant|>"),
        prompt="<|user|>\n{query}<|end|>\n<|assistant|>\n",
        sep="<|end|>\n",
        stop_str="<|end|>",
    )
)

"""llama2 template
Supports: https://huggingface.co/meta-llama/Llama-2-7b-chat-hf
          https://huggingface.co/meta-llama/Llama-2-13b-chat-hf
          https://huggingface.co/meta-llama/Llama-2-70b-chat-hf
reference: https://github.com/facebookresearch/llama/blob/cfc3fc8c1968d390eb830e65c63865e980873a06/llama/generation.py#L212
"""
register_conv_template(
    Conversation(
        name="llama2",
        system_prompt=(
            "<<SYS>>\nYou are a helpful, respectful and honest assistant. "
            "Always answer as helpfully as possible, while being safe. "
            "Your answers should not include any harmful, unethical, racist, sexist, "
            "toxic, dangerous, or illegal content. "
            "Please ensure that your responses are socially unbiased and positive in nature.\n\n"
            "If a question does not make any sense, or is not factually coherent, "
            "explain why instead of answering something not correct. "
            "If you don't know the answer to a question, please don't share false information.\n<</SYS>>\n\n"
        ),
        messages=[],
        roles=("[INST]", "[/INST]"),
        prompt="[INST] {query} [/INST]",
        sep="</s>",
    )
)

"""llama3 template
source: https://huggingface.co/meta-llama
Supports: https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct
chat template:
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{{ system_prompt }}<|eot_id|><|start_header_id|>user<|end_header_id|>
{{ user_msg_1 }}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
{{ model_answer_1 }}<|eot_id|>
"""
register_conv_template(
    Conversation(
        name="llama3",
        system_prompt=(
            "<|start_header_id|>system<|end_header_id|>\n\n"
            "You are a helpful, excellent and smart assistant."
        ),
        messages=[],
        roles=("user", "assistant"),
        prompt=(
            "<|start_header_id|>user<|end_header_id|>\n\n{query}<|eot_id|>"
            "<|start_header_id|>assistant<|end_header_id|>\n\n"
        ),
        sep="<|eot_id|>",
        stop_str="<|eot_id|>",
    )
)

"""llama2-zh template
source: https://github.com/ymcui/Chinese-LLaMA-Alpaca-2
Supports: https://huggingface.co/ziqingyang/chinese-alpaca-2-7b
"""
register_conv_template(
    Conversation(
        name="llama2-zh",
        system_prompt="[INST] <<SYS>>\nYou are a helpful assistant. 你是一个乐于助人的助手。\n<</SYS>>\n\n [/INST]",
        messages=[],
        roles=("[INST]", "[/INST]"),
        prompt="[INST] {query} [/INST]",
        sep="</s>",
    )
)

"""mistral template
Supports: https://huggingface.co/mistralai/Mistral-7B-v0.1
          https://huggingface.co/HuggingFaceH4/zephyr-7b-beta
source: https://docs.mistral.ai/llm/mistral-instruct-v0.1
"""
register_conv_template(
    Conversation(
        name="mistral",
        system_prompt="",
        messages=[],
        roles=("[INST]", "[/INST]"),
        prompt="[INST] {query} [/INST]",
        sep="</s>",
    )
)

"""XVERSE template
Supports: https://huggingface.co/xverse/XVERSE-13B-Chat
"""
register_conv_template(
    Conversation(
        name="xverse",
        system_prompt="",
        messages=[],
        roles=("Human", "Assistant"),
        prompt="Human: {query}\n\nAssistant: ",
        sep="</s>",
    )
)

"""Qwen template
Supports: https://huggingface.co/Qwen/Qwen-7B-Chat
chatml: https://xbot123.com/645a461b922f176d7cfdbc2d/
"""
register_conv_template(
    Conversation(
        name="chatml",
        system_prompt="You are a helpful assistant.",
        messages=[],
        roles=("user", "assistant"),
        prompt="<|im_start|>user\n{query}<|im_end|>\n<|im_start|>assistant\n",
        sep="<|im_end|>\n",
        stop_str="<|im_end|>",
    )
)

"""deepseek template
Supports: https://huggingface.co/deepseek-ai/deepseek-llm-7b-chat
          https://huggingface.co/deepseek-ai/deepseek-moe-16b-chat
"""
register_conv_template(
    Conversation(
        name="deepseek",
        system_prompt="",
        messages=[],
        roles=("User", "Assistant"),
        prompt="User: {query}\n\nAssistant:",
        sep="</s>",
    )
)

"""deepseekcoder template
Supports: https://huggingface.co/deepseek-ai/deepseek-coder-33b-instruct
"""
register_conv_template(
    Conversation(
        name="deepseekcoder",
        system_prompt=(
            "You are an AI programming assistant, utilizing the Deepseek Coder model, "
            "developed by Deepseek Company, and you only answer questions related to computer science. "
            "For politically sensitive questions, security and privacy issues, "
            "and other non-computer science questions, you will refuse to answer\n"
        ),
        messages=[],
        roles=("### Instruction", "### Response"),
        prompt="### Instruction:\n{{content}}\n### Response:\n",
        sep="\n",
        stop_str="<|EOT|>",
    )
)

"""Yi template
source: https://github.com/01-ai/Yi
Supports: https://huggingface.co/01-ai/Yi-34B-Chat
          https://huggingface.co/01-ai/Yi-6B-Chat
"""
register_conv_template(
    Conversation(
        name="yi",
        system_prompt="",
        messages=[],
        roles=("user", "assistant"),
        prompt="<|im_start|>user\n{query}<|im_end|>\n<|im_start|>assistant\n",
        sep="\n",
        stop_str="<|im_end|>",
    )
)

"""Orion template
source: https://github.com/OrionStarAI/Orion
Supports: https://huggingface.co/OrionStarAI/Orion-14B-Chat
"""
register_conv_template(
    Conversation(
        name="orion",
        system_prompt="",
        messages=[],
        roles=("Human", "Assistant"),
        prompt="Human: {query}\n\nAssistant: </s>",
        sep="</s>",
    )
)

"""Cohere template
source: https://huggingface.co/CohereForAI/c4ai-command-r-plus
Supports: https://huggingface.co/CohereForAI/c4ai-command-r-plus-4bit
          https://huggingface.co/CohereForAI/c4ai-command-r-plus
"""
register_conv_template(
    Conversation(
        name="cohere",
        system_prompt="<BOS_TOKEN>",
        messages=[],
        roles=("User", "Assistant"),
        prompt=(
            "<|START_OF_TURN_TOKEN|><|USER_TOKEN|>{query}<|END_OF_TURN_TOKEN|>"
            "<|START_OF_TURN_TOKEN|><|CHATBOT_TOKEN|>"
        ),
        sep="</s>",
    )
)

"""Qwen template
source: https://huggingface.co/Qwen/CodeQwen1.5-7B-Chat/blob/main/tokenizer_config.json#L18
Supports: https://huggingface.co/Qwen/CodeQwen1.5-7B-Chat
"""
register_conv_template(
    Conversation(
        name="qwen",
        system_prompt="<|im_start|>system\nYou are a helpful assistant.<|im_end|>\n",
        messages=[],
        roles=("user", "assistant"),
        prompt="<|im_start|>user\n{query}<|im_end|>\n<|im_start|>assistant\n",
        sep="\n",
        stop_str="<|im_end|>",
    )
)


def get_conv_template(name: str) -> Conversation:
    """Get a conversation template."""
    return conv_templates[name]
