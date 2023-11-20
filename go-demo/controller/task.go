package controller

import (
	"encoding/json"
	"fmt"
	"github.com/Steven147/demos/go-demo/model"
	larkapplication "github.com/larksuite/oapi-sdk-go/v3/service/application/v6"
	larkim "github.com/larksuite/oapi-sdk-go/v3/service/im/v1"
)

func getOptionSuggest(str string) string {
	// todo move to keva clientModel
	return ""
}

type TaskController struct {
	clientModel *model.ClientModel
	cardModel   *model.CardModel
	// todo add keva clientModel
}

func NewTaskController() *TaskController {
	return &TaskController{
		clientModel: model.NewClientModel(),
		cardModel:   model.NewCardModel(),
	}
}

func (taskController *TaskController) BotMenuTask(event *larkapplication.P2BotMenuV6) {
	key := *event.Event.EventKey
	userId := *event.Event.Operator.OperatorId.UserId
	taskController.sendDocGuide(userId, "user_id", key)
}

func (taskController *TaskController) MessageReceiveTask(event *larkim.P2MessageReceiveV1) {
	var result map[string]interface{}
	err := json.Unmarshal([]byte(*event.Event.Message.Content), &result)
	if err != nil {

	}
	content := result["text"]
	chatId := *event.Event.Message.ChatId
	if content == model.CardPrefix {
		taskController.clientModel.CreateMessageReqWrapper(
			"chat_id", chatId, "interactive", taskController.cardModel.GeneratedCard(),
		)
	}
}

//type CardsMap = map[string]struct {
//	category     string
//	section      string
//	relationship string
//	className    string
//}
//
//var cardsMap = CardsMap{}
//
//func (taskController *TaskController) CardActionTask(card larkcard.CardAction) {
//	action := card.Action
//	tag := action.Tag
//	openMessageId := card.OpenMessageID
//	open_chat_id := card.OpenChatId
//	if tag == "button" {
//		record := cardsMap[openMessageId]
//		mappedCategory, mapped_section, mapped_relationship, mapped_parent_token :=
//			record.category, record.section, record.relationship, record.className
//
//	}
//
//}

func (taskController *TaskController) sendDocGuide(chatId string, receiveType string, key string) {

	guideStr1NewDoc := fmt.Sprintf(
		`1. 分别输入文档信息，生成编码。\n`+
			`-%s\n`+
			`-%s\n`+
			`-%s\n`+
			`-%s\n`+
			`-请输入标题\n`+
			`例如发送消息\n`+
			`<<<%s秘笈、爱未来、生命成长类、未来八期、中国当代青年的样子\n`+
			`自动回复\n`+
			`>>>生成编码和标题：A0403001中国当代青年的样子\n`+
			`>>>生成知识库链接：... \n`,

		getOptionSuggest(model.Mappings["category"]),
		getOptionSuggest(model.Mappings["section"]),
		getOptionSuggest(model.Mappings["relationship"]),
		getOptionSuggest(model.Mappings["class_name"]),
		model.NewDocPrefix,
	)

	guideStr2SearchDoc := fmt.Sprintf(
		`2.1 输入编码，查询文章\\n`+
			`例如发送消息\n`+
			`<<<%sA0403001\n`+
			`自动回复文档查询结果\n`+
			`>>>查询到的编码和标题：A0403001中国当代青年的样子\n`+
			`>>>查询到的知识库链接：...\n`+
			`2.2 输入课程，查询所有文章\n`+
			`-%s\n`+
			`例如发送消息\n`+
			`<<<%s未来八期\n`+
			`会自动回复课程内的所有文档结果\n`,

		model.SearchDocPrefix,
		getOptionSuggest(model.Mappings["class_name"]),
		model.MultiSearchDocPrefix,
	)

	guideStr3OutputDoc := fmt.Sprintf(
		`3.1 输入编码，导出文档\n`+
			`例如发送消息\n`+
			`<<<%sA0403001\n`+
			`自动回复文档文件\n`+
			`>>>[A0403001中国当代青年的样子.pdf]\n`+
			`3.2 输入课程名，导出所有文档\n`+
			`例如发送消息\n`+
			`<<<%s未来八期\n`+
			`会自动回复课程内的所有文档文件\n`,

		model.OutputDocPrefix,
		model.MultiOutputDocPrefix,
	)

	guideStr := `命令帮助\n`

	if key == "menu0201" || key == "default" {
		guideStr += guideStr1NewDoc + `\n` + guideStr2SearchDoc + `\n` + guideStr3OutputDoc
	} else if key == "menu0202" {
		guideStr += guideStr1NewDoc
	} else if key == "menu0203" {
		guideStr += guideStr2SearchDoc
	} else if key == "menu0204" {
		guideStr += guideStr3OutputDoc
	} else {
		return
	}

	taskController.clientModel.CreateMessageReqWrapper(receiveType, chatId, "text", fmt.Sprintf(`{"text":"%s"}`, guideStr))
}
