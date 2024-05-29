from transformers import pipeline


class Instruction:
    def __init__(self):
        # 设置模型和生成器
        self.generator = pipeline('text-generation',
                                  model='uer/gpt2-chinese-cluecorpussmall',
                                  tokenizer='uer/gpt2-chinese-cluecorpussmall',
                                  device=0)  # 如果有多个GPU，可以切换到不同的GPU

    def get_instruction(self, prompt, num, length):
        # 生成文本
        result = self.generator(prompt, max_length=length, num_return_sequences=num)
        # 输出文本
        generated_text = result[0]['generated_text']
        return generated_text


def main():
    # 设置模型和生成器
    generator = pipeline('text-generation',
                         model='uer/gpt2-chinese-cluecorpussmall',
                         tokenizer='uer/gpt2-chinese-cluecorpussmall',
                         device=0)  # 如果有多个GPU，可以切换到不同的GPU
    # 设置主题
    prompt = "好的"
    # 生成文本
    result = generator(prompt, max_length=50, num_return_sequences=1)
    # 输出文本
    generated_text = result[0]['generated_text']
    print(generated_text)


if __name__ == '__main__':
    main()
