# start java environment

[廖雪峰的官方网站](liaoxuefeng.com/wiki/1252599548343744/)

## version of java

- Java SE: Standard Edition
- Java EE: Enterprise Edition
- Java ME: Micro Edition

```s 
which java
asdf which java
```

- Time	Version
- 1995	1.0
- 1998	1.2
- 2000	1.3
- 2002	1.4
- 2004	1.5 / 5.0
- 2005	1.6 / 6.0
- 2011	1.7 / 7.0
- 2014	1.8 / 8.0
- 2017/9	1.9 / 9.0
- 2018/3	10
- 2018/9	11
- 2019/3	12
- 2019/9	13
- 2020/3	14
- 2020/9	15
- 2021/3	16
- 2021/9	17
- 2022/3	18
- 2022/9	19

## learning map

learning map of Java
- Java SE: Java language / Java Core Functionality / Java Standard Library
  - Android: Android Develop
  - Java EE: Spring / Sql ...
  - Java Analysis: Hadoop / Spark / Flink ...

## Words Explain

JDK: Java Development Kit
JRE: Java Runtime Environment
JVM: Java Virtual Machine
```
  ┌─    ┌──────────────────────────────────┐
  │     │     Compiler, debugger, etc.     │
  │     └──────────────────────────────────┘
 JDK ┌─ ┌──────────────────────────────────┐
  │  │  │                                  │
  │ JRE │      JVM + Runtime Library       │
  │  │  │                                  │
  └─ └─ └──────────────────────────────────┘
        ┌───────┐┌───────┐┌───────┐┌───────┐
        │Windows││ Linux ││ macOS ││others │
        └───────┘└───────┘└───────┘└───────┘
/bin❯ ls   
jar         jconsole    jinfo       jshell      rmid
jarsigner   jdb         jjs         jstack      rmiregistry
java        jdeprscan   jlink       jstat       serialver
javac       jdeps       jmap        jstatd      unpack200
javadoc     jfr         jmod        keytool
javap       jhsdb       jps         pack200
jcmd        jimage      jrunscript  rmic
```

java：这个可执行程序其实就是JVM，运行Java程序，就是启动JVM，然后让JVM执行指定的编译后的代码；
javac：这是Java的编译器，它用于把Java源码文件（以.java后缀结尾）编译为Java字节码文件（以.class后缀结尾）；
jar：用于把一组.class文件打包成一个.jar文件，便于发布；
javadoc：用于从Java源码中自动提取注释并生成文档；
jdb：Java调试器，用于开发阶段的运行调试。

```java
// 一个Java源码只能定义一个public类型的class，并且class名称和文件名要完全一致
public class Hello { 
    public static void main(String[] args) {
        System.out.println("Hello, world!");
		// 方法的代码每一行用;结束
    }
}
```

```s
javac Hello.java # compile
java Hello.class # execute

┌──────────────────┐
│    Hello.java    │◀── source code
└──────────────────┘
          │ compile
          ▼
┌──────────────────┐
│   Hello.class    │◀── byte code
└──────────────────┘
          │ execute
          ▼
┌──────────────────┐
│    Run on JVM    │
└──────────────────┘
```
