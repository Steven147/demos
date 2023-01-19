package singleton.testSingleton

/**
 * Created by linshaoqin on 12/11/22
 * @author linshaoqin@bytedance.com
 */
class singletion3 {
    // 伴生对象不能理解成嵌套的对象，应该理解成给静态变量划的区域（在java中是概念，在kt中是个实际的区域）
    companion object {
        private var instance: singletion3? = null
            @Synchronized
            get() { // companion 伴生对象声明时，内部已有getInstance / setInstance方法，此处override
                // field 用在属性访问器内部来引用该属性的幕后字段; it 用在lambda 表达式内部来隐式引用其参数
                if (field == null) {
                    field = singletion3()
                }
                return field
            }
    }
}