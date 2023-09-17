package com.linshaoqin.myapp

import android.util.Log

object LogWrapper {
    fun debug(message: String? = null, tag: String? = null) {
        val stackTrace = Thread.currentThread().stackTrace
        val element = stackTrace[4]
        val tagOrClass = if (tag.isNullOrEmpty()) element.className else tag
        val methodInfo = "Class: ${element.className}, Method: ${element.methodName}"
        Log.d(tagOrClass, "[$methodInfo] $message")
    }
}