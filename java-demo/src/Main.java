import singleton.testSingleton.singleton;

/**
 * Created by linshaoqin on $DATE
 *
 * @author linshaoqin@bytedance.com
 */
public class Main {
    // static 静态变量
    public static void main(String[] args) {
        System.out.println("Hello world!");
        init();
    }

    public static void init() {
        var inst1 = singleton.getInstance();
        var inst2 = singleton.getInstance();
    }
}