package com.linshaoqin.myapp

import android.util.Log

object LogWrapper {
    fun debug(message: String = "", tag: String? = null) {
        val stackTrace = Thread.currentThread().stackTrace
        val element = stackTrace[4]
        val className = element.className
        val simpleClassName = className.substring(className.lastIndexOf('.') + 1)
        val tagOrClass = if (tag.isNullOrEmpty()) {
            "linshaoqin.${simpleClassName}"
        } else {
            tag
        }
        val methodInfo = "Class: ${simpleClassName}, Method: ${element.methodName}"
        Log.d(tagOrClass, "[$methodInfo] $message")
    }
}