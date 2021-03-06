from samson.math.algebra.rings.ring import Ring, RingElement, left_expression_intercept
from samson.math.general import totient

class MultiplicativeGroupElement(RingElement):
    """
    Element of a `MultiplicativeGroup`.
    """

    def __init__(self, val: int, ring: Ring):
        """
        Parameters:
            val   (int): Value of the element.
            ring (Ring): Parent ring.
        """
        self.ring = ring
        self.val  = val


    def __repr__(self):
        return f"<MultiplicativeGroupElement: val={self.val}, ring={self.ring}>"


    @left_expression_intercept
    def __add__(self, other: object) -> object:
        other = self.ring.coerce(other)
        return MultiplicativeGroupElement(self.val * other.val, self.ring)

    @left_expression_intercept
    def __sub__(self, other: object) -> object:
        other = self.ring.coerce(other)
        return MultiplicativeGroupElement(self.val / other.val, self.ring)

    def __mul__(self, other: object) -> object:
        other = int(other)
        if self.ring.order_cache:
            other %= self.ring.order_cache

        return MultiplicativeGroupElement(self.val ** other, self.ring)

    def __neg__(self) -> object:
        return MultiplicativeGroupElement(~self.val, self.ring)


    @left_expression_intercept
    def __truediv__(self, other: object) -> object:
        from samson.math.general import pohlig_hellman

        g = self.ring.coerce(other)
        return pohlig_hellman(g, self, self.ring.order)


    __floordiv__ = __truediv__

    def ordinality(self) -> int:
        return self.val.ordinality() - 1


    def is_invertible(self) -> bool:
        """
        Determines if the element is invertible.

        Returns:
            bool: Whether the element is invertible.
        """
        return self.val.is_invertible()


class MultiplicativeGroup(Ring):
    """
    The group of a ring under multiplication. This basically just 'promotes' multiplication to the addition operator.

    Examples:
        >>> from samson.math.all import *
        >>> a, b = 36, 9
        >>> ring = ZZ/ZZ(53)
        >>> mul_ring = ring.mul_group()
        >>> g = mul_ring(2)
        >>> (g*a)*(g*b) # Perform Diffie-Hellman
        <MultiplicativeGroupElement: val=ZZ(15), ring=ZZ/ZZ(53)*>

    """

    def __init__(self, ring: Ring):
        """
        Parameters:
            ring (Ring): Underlying ring.
        """
        self.ring        = ring
        self.order_cache = None


    @property
    def characteristic(self) -> int:
        return self.ring.characteristic


    @property
    def order(self) -> int:
        from samson.math.algebra.rings.quotient_ring import QuotientRing
        from samson.math.algebra.rings.integer_ring import IntegerElement
        from samson.math.polynomial import Polynomial
        from samson.math.symbols import oo

        if not self.order_cache:
            if type(self.ring) is QuotientRing:
                quotient = self.ring.quotient

                if type(quotient) is IntegerElement:
                    self.order_cache = totient(int(quotient))

                elif type(quotient) is Polynomial:
                    if quotient.is_prime():
                        self.order_cache = int(quotient) - 1

                    else:
                        self.order_cache = totient(int(quotient))

                else:
                    raise NotImplementedError()

            elif self.ring.order == oo:
                self.order_cache = oo

            else:
                raise NotImplementedError()

        return self.order_cache


    def zero(self) -> MultiplicativeGroupElement:
        """
        Returns:
            MultiplicativeGroupElement: '0' element of the algebra.
        """
        return MultiplicativeGroupElement(self.ring.one(), self)


    def one(self) -> MultiplicativeGroupElement:
        """
        Returns:
            MultiplicativeGroupElement: '1' element of the algebra.
        """
        return self.zero()


    def __repr__(self):
        return f"<MultiplicativeGroup: ring={self.ring}>"


    def shorthand(self) -> str:
        return f'{self.ring}*'


    def coerce(self, other: object) -> MultiplicativeGroupElement:
        """
        Attempts to coerce other into an element of the algebra.

        Parameters:
            other (object): Object to coerce.
        
        Returns:
            MultiplicativeGroupElement: Coerced element.
        """
        from samson.math.algebra.rings.quotient_ring import QuotientRing

        if type(other) is int and type(self.ring) is QuotientRing:
            other %= self.ring.quotient

        if type(other) is not MultiplicativeGroupElement:
            other = MultiplicativeGroupElement(self.ring.coerce(other), self)
        return other


    def element_at(self, x: int) -> MultiplicativeGroupElement:
        """
        Returns the `x`-th element of the set.

        Parameters:
            x (int): Element ordinality.
        
        Returns:
           MultiplicativeGroupElement: The `x`-th element.
        """
        return self(self.ring[x+1])

    def __eq__(self, other: object) -> bool:
        return type(self) == type(other) and self.ring == other.ring


    def __hash__(self) -> int:
        return hash((self.ring, self.__class__))
