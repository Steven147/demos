package model

var (
	NewDocPrefix         = "编码："
	SearchDocPrefix      = "查询："
	MultiSearchDocPrefix = "批量查询："
	OutputDocPrefix      = "导出："
	MultiOutputDocPrefix = "批量导出："
)

var Mappings = map[string]string{
	"category":     "your_category",
	"section":      "your_section",
	"relationship": "your_relationship",
	"class_name":   "your_class_name",
}

type KevaModel struct {
}
