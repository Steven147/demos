package singleton.testSingleton4;

/**
 * Created by linshaoqin on 12/11/22
 *
 * @author linshaoqin@bytedance.com
 */
public class singleton4 {
    private volatile static singleton4 instance;
    private singleton4(){}
    public static singleton4 getInstance(){
        if(instance==null){
            synchronized (singleton4.class){
                if(instance==null){
                    instance=new singleton4();
                }
            }
        }
        return instance;
    }
}
