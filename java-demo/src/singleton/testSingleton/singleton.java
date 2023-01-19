package singleton.testSingleton;

/**
 * Created by linshaoqin on 11/11/22
 *
 * @author linshaoqin@bytedance.com
 */
//1饿汉模式：创建时初始化，final 修饰后，变量不可重复赋值 / 方法不可重写 / 类不可继承
public class singleton {
    private static final singleton INSTANCE = new singleton();

    private singleton() {
    }

    public static singleton getInstance() {
        return INSTANCE;
    }
}

