class Tag:
	def __init__(self, name='tag', is_single=False, output='', **attributes):
		self.name = name
		self.text = ''
		self.children = []
		self.is_child = False
		self.attributes = attributes
		self.is_single = is_single
		self.output = output
		
	def __enter__(self):
		return self

	def __exit__(self, *args):
		if not self.is_child:
			child_str = ''.join(map(str, self.children))
			if self.is_single:
				print(f'<{self.name}{self.finally_attr()}>\n')
			else:
				print(f'<{self.name}{self.finally_attr()}>\n{child_str}\n</{self.name}>')

	def __iadd__(self, other):
		self.children.append(other)
		other.is_child = True
		return self

	def __str__(self):
		if self.children:
			child_str = ''.join(map(str, self.children)) 
			return f'<{self.name}{self.finally_attr()}>\n{self.text}{child_str}\n</{self.name}>'
		else:
			if self.is_single:
				return f'<{self.name}{self.finally_attr()}>'
			else:
				return f'<{self.name}{self.finally_attr()}>{self.text}</{self.name}>'

	def finally_attr(self):
		if self.attributes:
			attr_list = ' '
			for attr, value in self.attributes.items():				
				if attr == 'klass':
					attr = 'class'
					value = ' '.join(self.attributes['klass'])
				attr_list += f'{attr}="{value}" '
			return attr_list
		else:
			return ''

class TopLevelTag(Tag):
	pass

class HTML(Tag):
	
	def __enter__(self):
		return self

	def __exit__(self, *args):
		child_str = ''.join(map(str, self.children))
		if self.output:
			with open(self.output, 'w') as out_file:
				print(f'<html{self.finally_attr()}>\n{child_str}\n</html>', file = out_file)
		else:
			print(f'<html{self.finally_attr()}>\n{child_str}\n</html>')






with HTML(output='test.html') as doc: #если задать output=None html код выведется в консоль

	with TopLevelTag("head") as head:
		with Tag("title") as title:
			title.text = "hello"
			head += title
		doc += head


	with TopLevelTag("body") as body:
		with Tag("h1", klass=("main-text",)) as h1:
			h1.text = "Test"
			body += h1

		with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
			with Tag("p") as paragraph:
				paragraph.text = "another test"
				div += paragraph

			with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
				div += img
			body += div
		doc += body