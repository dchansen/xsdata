import sys

import pytest

from tests.testcases import ModelTestCase
from xsdata.models.elements import (
    AnnotationBase,
    Attribute,
    BaseModel,
    ComplexContent,
    ComplexType,
    Element,
    Extension,
    MinLength,
    Pattern,
    Restriction,
    Schema,
    Sequence,
    SimpleContent,
    SimpleType,
)
from xsdata.schema import SchemaReader


class ComplexTypeTests(ModelTestCase):
    result: BaseModel

    @classmethod
    def setUpClass(cls) -> None:
        xsd = cls.fixture_path("complex_types")
        reader = SchemaReader(xsd)
        cls.result = reader.parse()

    def setUp(self) -> None:
        self.assertIsInstance(self.result, Schema)

    def test_with_sequence(self):
        actual: ComplexType = self.result.complex_types[0]

        expected = ComplexType.build(
            name="allowablePointsOfSaleType",
            sequence=Sequence.build(
                max_occurs=sys.maxsize,
                elements=[
                    Element.build(
                        name="PointOfSale",
                        complex_type=ComplexType.build(
                            attributes=[
                                Attribute.build(name="id", type="xs:string")
                            ]
                        ),
                    )
                ],
            ),
        )
        self.assertEqual(expected, actual)
        self.assertIsInstance(actual, AnnotationBase)

    def test_with_simple_content_extension(self):
        actual: ComplexType = self.result.complex_types[1]

        expected = ComplexType.build(
            name="priceCurrencyType",
            simple_content=SimpleContent.build(
                extension=Extension.build(
                    base="priceType",
                    attributes=[
                        Attribute.build(
                            name="currency",
                            use="required",
                            simple_type=SimpleType.build(
                                restriction=Restriction.build(
                                    base="xs:string",
                                    pattern=Pattern("[A-Z][A-Z][A-Z]"),
                                )
                            ),
                        )
                    ],
                )
            ),
        )
        self.assertEqual(expected, actual)

    @pytest.mark.skip(reason="Missing sample")
    def test_with_simple_content_restriction(self):
        pass

    def test_with_complex_content_extension(self):
        actual: ComplexType = self.result.complex_types[2]

        expected = ComplexType.build(
            name="UserRateConditionType",
            complex_content=ComplexContent.build(
                extension=Extension.build(
                    base="UserRateConditionBaseType",
                    attributes=[
                        Attribute.build(
                            name="id",
                            use="required",
                            simple_type=SimpleType.build(
                                restriction=Restriction.build(
                                    base="xs:string", min_length=MinLength(1)
                                )
                            ),
                        )
                    ],
                )
            ),
        )
        self.assertEqual(expected, actual)

    @pytest.mark.skip(reason="Missing sample")
    def test_with_complex_content_restriction(self):
        pass
