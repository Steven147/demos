package singleton.testSingleton3;

// 2懒汉模式：在使用时初始化 3synchronized使用同步锁线程安全
public class singleton3 {
    private static singleton3 INSTANCE = null;

    private singleton3() {
    }

    public static synchronized singleton3 getInstance() {
        if (INSTANCE == null) {
            INSTANCE = new singleton3();
        }
        return INSTANCE;
    }
}
