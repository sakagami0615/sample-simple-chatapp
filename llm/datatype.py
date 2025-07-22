from dataclasses import dataclass


@dataclass
class ModelInfo:
    """モデル情報格納クラス"""

    model_name: str
    temperature: float

    def __copy__(self):
        """コピーメソッド

        copyを使用した場合、浅いコピーではなく深いコピーされるようにカスタムしている。
        """
        return type(self)(
            model_name=self.model_name,
            temperature=self.temperature,
        )
