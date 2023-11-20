package model

import (
	jsoniter "github.com/json-iterator/go"
	"log"
)

type CardExtras map[string]struct {
	Text        string
	Placeholder string
	Options     map[string]string
}

func NewGenerateDocCard() *CardExtras {
	return &CardExtras{
		"category": {
			Text:        "请输入文档分类",
			Placeholder: "文档分类",
			Options: map[string]string{
				"秘笈": "A",
				"表达": "B",
				"行为": "C",
				"操作": "D",
			},
		},
		"section": {
			Text:        "请输入版块",
			Placeholder: "版块",
			Options: map[string]string{
				"爱相伴": "01",
				"爱相随": "02",
				"爱相遇": "03",
				"爱未来": "04",
				"不确定": "05",
			},
		},
		"relationship": {
			Text:        "请输入关系",
			Placeholder: "关系",
			Options: map[string]string{
				"生命成长类": "01",
				"亲子关系类": "02",
				"孝亲关系类": "03",
				"夫妻关系类": "04",
				"通用关系类": "05",
			},
		},
		"class_name": {
			Text:        "请输入课程名称",
			Placeholder: "课程名称",
			Options: map[string]string{
				"网络七期": "VwrUwqamZiGRpGkndmGcFBJhn2d",
				"未来八期": "LU46wq2kIixvGVkfenqcX4bMnfc",
			},
		},
	}
}

func (mappings CardExtras) GenerateElements() []map[string]interface{} {
	var elements []map[string]interface{}

	for key, details := range mappings {
		var options []map[string]interface{}

		for text, value := range details.Options {
			option := map[string]interface{}{
				"text": map[string]interface{}{
					"tag":     "plain_text",
					"content": text,
				},
				"value": value,
			}
			options = append(options, option)
		}

		element := map[string]interface{}{
			"tag": "div",
			"text": map[string]interface{}{
				"tag":     "lark_md",
				"content": details.Text,
			},
			"extra": map[string]interface{}{
				"tag": "select_static",
				"placeholder": map[string]interface{}{
					"tag":     "plain_text",
					"content": details.Placeholder,
				},
				"value": map[string]interface{}{
					"key": key,
				},
				"options": options,
			},
		}
		elements = append(elements, element)
	}

	elements = append(elements, map[string]interface{}{
		"tag": "div",
		"text": map[string]interface{}{
			"tag":     "lark_md",
			"content": "选择完成后，点击确认，会自动生成文档对应的编码" + "\n同时会以编码作为标题在知识库中新建文档，返回文档链接。",
		},
		"extra": map[string]interface{}{
			"tag": "button",
			"text": map[string]interface{}{
				"tag":     "lark_md",
				"content": "确认",
			},
			"type": "primary",
			"value": map[string]interface{}{
				"key": "confirm",
			},
		},
	})

	return elements
}

func getCardSourceString(elements []map[string]interface{}) string {
	data := map[string]interface{}{
		"config": map[string]interface{}{
			"wide_screen_mode": true,
		},
		"header": map[string]interface{}{
			"template": "blue",
			"title": map[string]interface{}{
				"tag":     "plain_text",
				"content": "文档编码生成卡片",
			},
		},
		"card_link": map[string]interface{}{
			"url":         "",
			"pc_url":      "",
			"android_url": "",
			"ios_url":     "",
		},
		"elements": elements,
	}

	json := jsoniter.ConfigCompatibleWithStandardLibrary
	dataBytes, err := json.Marshal(data)
	if err != nil {
		log.Fatalf("JSON marshaling failed: %s", err)
	}

	return string(dataBytes)
}

type CardModel struct {
	generateDocCard *CardExtras
}

func (cardModel *CardModel) GeneratedCard() string {
	card := *cardModel.generateDocCard
	generatedElements := card.GenerateElements()
	return getCardSourceString(generatedElements)
}

func NewCardModel() *CardModel {
	return &CardModel{
		generateDocCard: NewGenerateDocCard(),
	}
}
