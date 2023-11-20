package main // Declare a main package

import (
	"context"
	"github.com/Steven147/demos/go-demo/controller"
	"github.com/gin-gonic/gin"
	sdkginext "github.com/larksuite/oapi-sdk-gin"
	"github.com/larksuite/oapi-sdk-go/v3/event/dispatcher"
	larkapplication "github.com/larksuite/oapi-sdk-go/v3/service/application/v6"
	larkim "github.com/larksuite/oapi-sdk-go/v3/service/im/v1"
)

var (
	verificationToken = "sIbA8tRAgaRNQo9MjKsZUbvYMTp1jXo0"
	eventEncryptKey   = ""
)

func main() {

	engine := gin.Default()

	RegisterRoutes(engine)
	err := engine.Run(":5000")

	if err != nil {
		return
	}
}

func RegisterRoutes(engine *gin.Engine) {
	taskController := controller.NewTaskController()
	// 注册消息处理器
	handler := dispatcher.NewEventDispatcher(
		verificationToken, eventEncryptKey,
	).OnP2MessageReceiveV1(func(ctx context.Context, event *larkim.P2MessageReceiveV1) error {
		// 处理消息 event
		go taskController.MessageReceiveTask(event)
		return nil
	}).OnP2BotMenuV6(func(ctx context.Context, event *larkapplication.P2BotMenuV6) error {
		// 处理消息 event
		go taskController.BotMenuTask(event)
		return nil
	})

	//// 创建card处理器
	//cardHandler := larkcard.NewCardActionHandler(
	//	verificationToken, eventEncryptKey,
	//	func(ctx context.Context, cardAction *larkcard.CardAction) (interface{}, error) {
	//
	//		// 创建卡片信息
	//		messageCard := larkcard.NewMessageCard().
	//			Build()
	//
	//		return messageCard, nil
	//	})
	engine.POST("/event", sdkginext.NewEventHandlerFunc(handler))
	//engine.POST("/card", sdkginext.NewCardActionHandlerFunc(cardHandler))
	engine.GET("/", func(c *gin.Context) {
		c.String(200, "Hello, World! Feishu Robot By linshaoqin")
	})
}

//func defaultTask(clientDelegate *model.ClientModel, event *larkim.P2MessageReceiveV1) {
//	chatId := *event.Event.Message.ChatId
//	fmt.Println(larkcore.Prettify(chatId))
//	clientDelegate.CreateMessageReqWrapper("chat_id", chatId, "text", "test")
//}
