package singleton.testSingleton4

/**
 * Created by linshaoqin on 12/11/22
 * @author linshaoqin@bytedance.com
 */
class singleton4kt private constructor(){
    companion object {
//        val instance: singleton4kt by lazy(mode = LazyThreadSafetyMode.SYNCHRONIZED) {
//            singleton4kt()
//        }

//        val instance: Lazy<singleton4kt>
//            get() {
//                return lazy(mode = LazyThreadSafetyMode.SYNCHRONIZED) {
//                    singleton4kt()
//                }
//            }
    }
}