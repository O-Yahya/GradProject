from Infer import Vulnerability

# creating lists of bug types reported by Infer based on their severity
high_severity = ["ARBITRARY_CODE_EXECUTION_UNDER_LOCK", "BUFFER_OVERRUN_L1", "BUFFER_OVERRUN_L2",
    "BUFFER_OVERRUN_L3", "BUFFER_OVERRUN_L4", "BUFFER_OVERRUN_L5", "CAPTURED_STRONG_SELF",
    "CROSS_SITE_SCRIPTING", "DANGLING_POINTER_DEREFERENCE", "DIVIDE_BY_ZERO",
    "EMPTY_VECTOR_ACCESS", "ERADICATE_NULLABLE_DEREFERENCE", "EXPENSIVE_LOOP_INVARIANT_CALL",
    "EXPOSED_INSECURE_INTENT_HANDLING", "GUARDEDBY_VIOLATION", "GUARDEDBY_VIOLATION_NULLSAFE",
    "IMPURE_FUNCTION", "INFERBO_ALLOC_IS_BIG", "INFERBO_ALLOC_IS_NEGATIVE",
    "INFERBO_ALLOC_IS_ZERO", "INFERBO_ALLOC_MAY_BE_BIG", "INFERBO_ALLOC_MAY_BE_NEGATIVE",
    "INSECURE_INTENT_HANDLING", "INTERFACE_NOT_THREAD_SAFE", "INVARIANT_CALL",
    "IVAR_NOT_NULL_CHECKED", "JAVASCRIPT_INJECTION", "LAB_RESOURCE_LEAK", "LOCK_CONSISTENCY_VIOLATION",
    "LOGGING_PRIVATE_DATA", "MEMORY_LEAK", "MIXED_SELF_WEAKSELF", "MULTIPLE_WEAKSELF",
    "NULLPTR_DEREFERENCE", "NULL_DEREFERENCE", "POINTER_TO_CONST_OBJC_CLASS",
    "PREMATURE_NIL_TERMINATION_ARGUMENT", "RESOURCE_LEAK", "RETAIN_CYCLE", "SHELL_INJECTION",
    "SQL_INJECTION", "SQL_INJECTION_RISK", "STACK_VARIABLE_ADDRESS_ESCAPE", "STARVATION",
    "STRICT_MODE_VIOLATION", "THREAD_SAFETY_VIOLATION", "THREAD_SAFETY_VIOLATION_NULLSAFE",
    "TOPL_ERROR", "UNTRUSTED_BUFFER_ACCESS", "UNTRUSTED_DESERIALIZATION",
    "UNTRUSTED_ENVIRONMENT_CHANGE_RISK", "UNTRUSTED_FILE", "UNTRUSTED_HEAP_ALLOCATION",
    "UNTRUSTED_INTENT_CREATION", "UNTRUSTED_URL_RISK", "UNTRUSTED_VARIABLE_LENGTH_ARRAY",
    "USER_CONTROLLED_SQL_RISK", "USE_AFTER_DELETE", "USE_AFTER_FREE", "USE_AFTER_LIFETIME",
    "VECTOR_INVALIDATION", "WEAK_SELF_IN_NO_ESCAPE_BLOCK"]

medium_severity = ["ASSIGN_POINTER_WARNING", "AUTORELEASEPOOL_SIZE_COMPLEXITY_INCREASE",
    "AUTORELEASEPOOL_SIZE_COMPLEXITY_INCREASE_UI_THREAD", "AUTORELEASEPOOL_SIZE_UNREACHABLE_AT_EXIT",
    "BAD_POINTER_COMPARISON", "BIABDUCTION_MEMORY_LEAK", "CHECKERS_ALLOCATES_MEMORY",
    "CHECKERS_ANNOTATION_REACHABILITY_ERROR", "CHECKERS_CALLS_EXPENSIVE_METHOD",
    "CHECKERS_EXPENSIVE_OVERRIDES_UNANNOTATED", "CHECKERS_FRAGMENT_RETAINS_VIEW",
    "CHECKERS_IMMUTABLE_CAST", "CHECKERS_PRINTF_ARGS", "CONSTANT_ADDRESS_DEREFERENCE",
    "CREATE_INTENT_FROM_URI", "CXX_REFERENCE_CAPTURED_IN_OBJC_BLOCK", "DEADLOCK",
    "DEAD_STORE", "DIRECT_ATOMIC_PROPERTY_ACCESS", "DISCOURAGED_WEAK_PROPERTY_CUSTOM_SETTER",
    "DOTNET_RESOURCE_LEAK", "ERADICATE_BAD_NESTED_CLASS_ANNOTATION", "ERADICATE_CONDITION_REDUNDANT",
    "ERADICATE_FIELD_NOT_INITIALIZED", "ERADICATE_FIELD_NOT_NULLABLE", "ERADICATE_FIELD_OVER_ANNOTATED",
    "ERADICATE_INCONSISTENT_SUBCLASS_PARAMETER_ANNOTATION", "ERADICATE_INCONSISTENT_SUBCLASS_RETURN_ANNOTATION",
    "ERADICATE_META_CLASS_CAN_BE_NULLSAFE", "ERADICATE_META_CLASS_IS_NULLSAFE",
    "ERADICATE_META_CLASS_NEEDS_IMPROVEMENT", "ERADICATE_PARAMETER_NOT_NULLABLE",
    "ERADICATE_REDUNDANT_NESTED_CLASS_ANNOTATION", "ERADICATE_RETURN_NOT_NULLABLE",
    "ERADICATE_RETURN_OVER_ANNOTATED", "ERADICATE_UNCHECKED_USAGE_IN_NULLSAFE",
    "ERADICATE_UNVETTED_THIRD_PARTY_IN_NULLSAFE", "EXPENSIVE_AUTORELEASEPOOL_SIZE",
    "EXPENSIVE_EXECUTION_TIME", "GLOBAL_VARIABLE_INITIALIZED_WITH_FUNCTION_OR_METHOD_CALL",
    "INEFFICIENT_KEYSET_ITERATOR", "MEMORY_LEAK", "NIL_MESSAGING_TO_NON_POD", "OPTIONAL_EMPTY_ACCESS",
    "PARAMETER_NOT_NULL_CHECKED", "PURE_FUNCTION", "QUANDARY_TAINT_ERROR", "RESOURCE_LEAK",
    "UNINITIALIZED_VALUE", "UNREACHABLE_CODE"
]

low_severity = ["COMPONENT_WITH_MULTIPLE_FACTORY_METHODS", "CONDITION_ALWAYS_FALSE", "CONDITION_ALWAYS_TRUE",
    "CONFIG_CHECKS_BETWEEN_MARKERS", "CONFIG_IMPACT", "ERADICATE_ANNOTATION_GRAPH",
    "ERADICATE_CONDITION_REDUNDANT", "EXECUTION_TIME_COMPLEXITY_INCREASE",
    "EXECUTION_TIME_COMPLEXITY_INCREASE_UI_THREAD", "EXECUTION_TIME_UNREACHABLE_AT_EXIT",
    "INTERFACE_NOT_THREAD_SAFE", "MODIFIES_IMMUTABLE", "MUTABLE_LOCAL_VARIABLE_IN_COMPONENT_FILE",
    "STRICT_MODE_VIOLATION", "THREAD_SAFETY_VIOLATION", "THREAD_SAFETY_VIOLATION_NULLSAFE"]

# creating dictionary
bug_severity_dict = {
    'high': high_severity,
    'medium': medium_severity,
    'low': low_severity
}

def calculate_security_score(vulnerabilities, bug_severity_dict):
    # security score variable which decreases based on vulnerabilities found
    score = 100

    if len(vulnerabilities) == 0:
        return score
    
    # weight assigned to each severity
    weights = {
        'high': 3,
        'medium': 2,
        'low': 1
    }

    # dictionary to store number of vulnerabilities of each severity found
    count = {
        'high': 0,
        'medium': 0,
        'low': 0
    }

    # iterating through vulnerabilities
    for vul in vulnerabilities:
        for severity, issues in bug_severity_dict.items():
            if vul.type in issues:
                count[severity] += 1
                break

    for severity, num in count.items():
        score -= num * weights[severity]

    score = max(0, score)
    return score