

@dataclass()
class Coord:
	col: int = field(default=1)
	row: int = field(default=1)

	def __str__(__s):
		return f'\x1b[{__s.y};{__s.x}H'
	@property
	def xy(__s) -> tuple[int, int]:
		return (__s.x, __s.y)
	@property
	def y(__s):
		return __s.row
	@property
	def x(__s):
		return __s.col