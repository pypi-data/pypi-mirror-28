# Daon

## Installation

```python
pip install daon
```

## Usage

```python
from daon import Tagger
tagger = Tagger()

tagger.pos(u'네, 안녕하세요. 반갑습니다.')

# 새로운 모델 적용 (모델 파일)
tagger = Tagger(model_path='/Users/mac/work/daon/daon-core/src/main/resources/daon/core/reader/model.dat')

# 새로운 모델 적용 (모델 url)
tagger = Tagger(url='http://localhost:5001/v1/model/download?seq=1514366867073')
```
