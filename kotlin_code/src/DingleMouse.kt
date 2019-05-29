class Dinglemouse {

    private val map: MutableMap<String, Any> = LinkedHashMap()

    fun setAge(age: Int): Dinglemouse = apply { map["age"] = age }

    fun setSex(sex: Char): Dinglemouse = apply { map["sex"] = sex }

    fun setName(name: String): Dinglemouse = apply { map["name"] = name }

    fun hello(): String {
        val seq = sequence {
            yield("Hello.")
            for (v in map.values) {
                when (v) {
                    is Int -> yield("I am $v.")
                    is Char -> yield("I am ${if (v == 'M') "male" else "female"}.")
                    is String -> yield("My name is $v.")
                }
            }
        }
        return seq.joinToString(" ")
    }
}
