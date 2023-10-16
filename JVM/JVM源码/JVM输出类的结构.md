[参考链接](https://gitee.com/wang-yi-656/openjdk/tree/traces/)中的classes分支

在InstanceKlass中插入代码

# 添加遍历字段函数traverse_fields

```C
void InstanceKlass::traverse_local_fields(FILE* classFile) const{
    ResourceMark rm;
    for (JavaFieldStream fs(this); !fs.done(); fs.next()) {
        char* f_name = fs.name()->as_C_string();
        char* f_type = fs.signature()->as_C_string();
        bool isStatic = fs.access_flags().is_static();
        fprintf(classFile, "    %s %s %s;\n", (isStatic? "static" : ""), f_type, f_name);
        resource_free_bytes(f_name, strlen(f_name) + 1);
        resource_free_bytes(f_type, strlen(f_type) + 1);
    }
}

void InstanceKlass::traverse_interface_fields(FILE* classFile) const {
    const int n = local_interfaces()->length();
    for (int i = 0; i < n; i++) {
        Klass* intf1 = local_interfaces()->at(i);
        assert(intf1->is_interface(), "just checking type");
        InstanceKlass::cast(intf1)->traverse_local_fields(classFile);
        InstanceKlass::cast(intf1)->traverse_interface_fields(classFile);
    }
}

void InstanceKlass::traverse_fields(FILE* classfile) const {
    // 1) traverse for field in current klass
    traverse_local_fields(classfile);
    // 2) traverse for field recursively in direct superinterfaces
    traverse_interface_fields(classfile);
    // 3) apply field traverse recursively if superclass exists
    { Klass* supr = super();
        if (supr != NULL) return InstanceKlass::cast(supr)->traverse_fields(classfile);
    }
}
```

# 在类初始化完成后调用遍历字段函数

即插入代码到初始化函数`void InstanceKlass::initialize_impl(TRAPS)`

````c
ResourceMark rm;
char* class_path = std::getenv("CLASS_PATH");
	char* class_name = this->name()->as_C_string();
	int name_length = this->name()->utf8_length();
    bool skip = false;
    // skip anonymous classes
	// for(int i = 0; i < name_length; i++){
	//   if(class_name[i] == '$'){
    //     skip = true;
    //   }
	// }
	if(skip == false){
      FILE* class_file = fopen(class_path, "a");
      if (class_file != NULL) {
        fprintf(class_file, "Class %s{\n", class_name);
        this->traverse_fields(class_file);
        fprintf(class_file, "}\n");
        fclose(class_file);
      } else {
        fprintf(stderr, "Failed to open the file. Please check CLASS_PATH environment.\n");
      }
    }
	resource_free_bytes(class_name, name_length);
````

![image-20231008201714183](D:%5CBackUp%5C%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%5C%E5%9B%BE%E7%89%87%5Cimage-20231008201714183.png)

