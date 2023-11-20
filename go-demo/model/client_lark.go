package model

import (
	"context"
	"fmt"
	lark "github.com/larksuite/oapi-sdk-go/v3"
	larkcore "github.com/larksuite/oapi-sdk-go/v3/core"
	larkdocx "github.com/larksuite/oapi-sdk-go/v3/service/docx/v1"
	larkim "github.com/larksuite/oapi-sdk-go/v3/service/im/v1"
)

type ClientModel struct {
	client *lark.Client
}

func NewClientModel() *ClientModel {
	client := lark.NewClient(
		"cli_a5bb0a8ac8f99013", "rceFwGZuDFcP1fYwjc812ftAsysPK1MZ",
		lark.WithEnableTokenCache(true), lark.WithLogLevel(larkcore.LogLevelDebug),
	)
	return &ClientModel{
		client: client,
	}
}

func (model *ClientModel) CreateDocumentBlockChildrenReqWrapper() {

	req := larkdocx.NewCreateDocumentBlockChildrenReqBuilder().Build()
	// 发起请求
	resp, err := model.client.Docx.DocumentBlockChildren.Create(context.Background(), req)
	// 处理错误
	if err != nil {
		fmt.Println(err)
		return
	}

	// 服务端错误处理
	if !resp.Success() {
		fmt.Println(resp.Code, resp.Msg, resp.RequestId())
		return
	}

	// 业务处理
	//fmt.Println(larkcore.Prettify(resp))
}

func (model *ClientModel) CreateMessageReqWrapper(
	receiveIdType string, receiveId string, msgType string, content string,
) {
	// 创建请求对象
	req := larkim.NewCreateMessageReqBuilder().
		ReceiveIdType(receiveIdType).
		Body(larkim.NewCreateMessageReqBodyBuilder().
			MsgType(msgType).
			ReceiveId(receiveId).
			Content(content).
			Build()).
		Build()

	// 发起请求
	resp, err := model.client.Im.Message.Create(context.Background(), req)
	// 处理错误
	if err != nil {
		fmt.Println(err)
		return
	}

	// 服务端错误处理
	if !resp.Success() {
		fmt.Println(resp.Code, resp.Msg, resp.RequestId())
		return
	}

	// 业务处理
	//fmt.Println(larkcore.Prettify(resp))
}
