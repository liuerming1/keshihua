/**
 * Import adapter for the reviewed PDF textbook JSON.
 *
 * This module deliberately does not adapt the rich textbook records to the
 * demo Knowledge model in index.ts.  The source contains information which
 * the demo model cannot represent safely (unknown dates, several themes,
 * page/image evidence and unlocated places), so this is a read-only, typed
 * data boundary for future consumers.
 */

export type HistoricalYear = number;
export type Coordinate = readonly [longitude: number, latitude: number];

export interface TextbookDocument {
  readonly id: string;
  readonly fileName: string | null;
  readonly title: string | null;
  readonly edition: string | null;
  readonly volume: string | null;
  readonly publisher: string | null;
  readonly publicationYear: HistoricalYear | null;
  readonly totalPdfPages: number | null;
  readonly language: string | null;
  readonly sourceKind: string | null;
  readonly sha256: string | null;
}

export interface TextbookPage {
  readonly id: string;
  readonly documentId: string | null;
  readonly pdfPageNumber: number | null;
  readonly printedPageLabel: string | null;
  readonly chapterPath: readonly string[];
  readonly pageKind: string | null;
  readonly textStatus: string | null;
  readonly imageStatus: string | null;
  readonly notes: readonly string[];
}

export interface TextbookEvidenceBlock {
  readonly id: string;
  readonly pageId: string | null;
  readonly order: number | null;
  readonly type: string | null;
  readonly bbox: unknown;
  readonly rawText: string | null;
  readonly cleanText: string | null;
  readonly assetIds: readonly string[];
  readonly tableData: unknown;
  readonly notes: readonly string[];
}

export interface TextbookAsset {
  readonly id: string;
  readonly pageId: string | null;
  readonly blockId: string | null;
  readonly type: string | null;
  readonly bbox: unknown;
  readonly filePath: string | null;
  readonly caption: string | null;
  readonly visibleText: string | null;
  readonly description: string | null;
  readonly claims: readonly unknown[];
  readonly notes: readonly string[];
}

export interface TextbookPlace {
  readonly id: string;
  readonly nameAsWritten: string;
  readonly nameType: string | null;
  readonly validTimeText: string | null;
  readonly coordinates: Coordinate | null;
  /** True only when the input explicitly marks the coordinates as verified. */
  readonly coordinatesVerified: boolean;
  readonly coordinateEvidenceBlockIds: readonly string[];
  readonly evidenceBlockIds: readonly string[];
  readonly notes: readonly string[];
}

export interface TextbookPlaceRef {
  readonly placeId: string;
  readonly role: string | null;
  readonly evidenceBlockIds: readonly string[];
}

export interface TextbookEvidenceText {
  readonly text: string;
  readonly evidenceBlockIds: readonly string[];
  readonly externalSourceIds: readonly string[];
}

export interface TextbookFinalization {
  readonly status: 'ready' | 'qualified' | 'needs_source' | string;
  readonly sourceVerificationStatus: string | null;
  readonly patchApplied: boolean;
  readonly factNote: string | null;
  readonly supplementalSourceIds: readonly string[];
}

export interface TextbookMapLayer {
  readonly id: string;
  readonly rasterAssetId: string;
  readonly rasterFilePath: string | null;
  readonly referenceTimeText: string | null;
  readonly referenceYear: HistoricalYear | null;
  readonly historicalNames: readonly string[];
  readonly imageLabels: readonly { text: string; imagePosition: Coordinate }[];
  readonly unmatchedHistoricalNames: readonly string[];
  readonly georeferenced: boolean;
  readonly geometryStatus: string | null;
  readonly reviewStatus: string | null;
  readonly referencePointIds: readonly string[];
}

export interface TextbookReferencePoint {
  readonly id: string;
  readonly name: string;
  readonly coordinates: Coordinate;
  readonly mapCandidateId: string;
  readonly temporalBasis: string | null;
  readonly historicalGeometry: boolean;
}

export interface TextbookExternalSource {
  readonly id: string;
  readonly title: string;
  readonly url: string;
}

export type TextbookKind = 'event' | 'process' | 'origin' | null;

export type TextbookTimeMode = 'point' | 'duration' | 'uncertain' | 'unknown' | string;

export type TextbookEndStatus = 'known' | 'ongoing' | 'unknown' | 'not_applicable' | string;

export interface TextbookTime {
  readonly sourceText: string | null;
  readonly mode: TextbookTimeMode;
  readonly startYear: HistoricalYear | null;
  readonly endYear: HistoricalYear | null;
  readonly earliestYear: HistoricalYear | null;
  readonly latestYear: HistoricalYear | null;
  readonly precision: string | null;
  readonly endStatus: TextbookEndStatus;
  readonly normalizationNote: string | null;
  readonly evidenceBlockIds: readonly string[];
}

export interface TextbookVerification {
  readonly overallStatus: string | null;
  readonly historicalStatus: string | null;
  readonly textbookAlignment: string | null;
  readonly confidence: string | null;
  readonly raw: Readonly<Record<string, unknown>>;
}

export interface TextbookKnowledge {
  readonly id: string;
  readonly title: string;
  readonly kind: TextbookKind;
  readonly contentType: string | null;
  readonly time: TextbookTime;
  readonly themes: readonly string[];
  readonly placeRefs: readonly TextbookPlaceRef[];
  readonly personIds: readonly string[];
  readonly summary: TextbookEvidenceText | null;
  readonly flow: readonly TextbookEvidenceText[];
  readonly points: readonly TextbookEvidenceText[];
  readonly background: TextbookEvidenceText | null;
  readonly impact: TextbookEvidenceText | null;
  readonly evidenceBlockIds: readonly string[];
  readonly assetIds: readonly string[];
  readonly sourceInventoryIds: readonly string[];
  readonly uncertainties: readonly string[];
  readonly reviewStatus: string | null;
  readonly verification: TextbookVerification | null;
  readonly finalization: TextbookFinalization | null;
}

export interface TextbookRelation {
  readonly id: string;
  readonly fromKnowledgeId: string;
  readonly toKnowledgeId: string | null;
  readonly targetLabel: string | null;
  readonly type: string | null;
  readonly personIds: readonly string[];
  readonly placeIds: readonly string[];
  readonly timeText: string | null;
  readonly description: string | null;
  readonly evidenceBlockIds: readonly string[];
  readonly reviewStatus: string | null;
}

export interface TextbookSourceInventory {
  readonly id: string;
  readonly documentId: string | null;
  readonly pageIds: readonly string[];
  readonly blockIds: readonly string[];
  readonly itemLabel: string | null;
  readonly scope: string | null;
  readonly disposition: string | null;
  readonly knowledgeIds: readonly string[];
  readonly duplicateOfInventoryId: string | null;
  readonly reason: string | null;
}

export interface TextbookMarker {
  readonly knowledgeId: string;
  readonly placeId: string;
  readonly title: string;
  readonly placeName: string;
  readonly coordinates: Coordinate;
  readonly coordinateEvidenceBlockIds: readonly string[];
}

export interface TextbookQuery {
  readonly startYear: HistoricalYear;
  readonly endYear: HistoricalYear;
  readonly theme?: string;
}

export interface TextbookQueryResult {
  readonly items: readonly TextbookKnowledge[];
  readonly excludedUnknownTime: readonly TextbookKnowledge[];
  readonly status: 'ready' | 'missing';
}

export interface TextbookMarkerQuery extends TextbookQuery {}

export interface TextbookRepository {
  readonly document: TextbookDocument | null;
  readonly documents: readonly TextbookDocument[];
  readonly pages: readonly TextbookPage[];
  readonly blocks: readonly TextbookEvidenceBlock[];
  readonly assets: readonly TextbookAsset[];
  readonly places: readonly TextbookPlace[];
  readonly knowledge: readonly TextbookKnowledge[];
  /** `items` is an intentional alias for consumers that use repository terminology. */
  readonly items: readonly TextbookKnowledge[];
  readonly relations: readonly TextbookRelation[];
  readonly inventory: readonly TextbookSourceInventory[];
  readonly mapLayers: readonly TextbookMapLayer[];
  readonly mapReferencePoints: readonly TextbookReferencePoint[];
  readonly externalSources: readonly TextbookExternalSource[];
  query(query: TextbookQuery): TextbookQueryResult;
  get(id: string): TextbookKnowledge | undefined;
  listUndated(theme?: string): readonly TextbookKnowledge[];
  /** Alias with a more explicit name for callers that do not use “undated”. */
  listUnknownTime(theme?: string): readonly TextbookKnowledge[];
  getEvidence(id: string): readonly TextbookEvidenceBlock[];
  getAssets(id: string): readonly TextbookAsset[];
  getMarkers(query: TextbookMarkerQuery): readonly TextbookMarker[];
  /** Return the outgoing relation targets for one knowledge item. */
  getRelated(itemOrId: TextbookKnowledge | string): readonly TextbookKnowledge[];
  /** Alias for map-oriented call sites. */
  getMapMarkers(query: TextbookMarkerQuery): readonly TextbookMarker[];
}

interface JsonObject {
  readonly [key: string]: unknown;
}

const isObject = (value: unknown): value is JsonObject =>
  typeof value === 'object' && value !== null && !Array.isArray(value);

const stringValue = (value: unknown): string | null => typeof value === 'string' ? value : null;

const stringArray = (value: unknown): readonly string[] =>
  Array.isArray(value) ? value.filter((entry): entry is string => typeof entry === 'string') : [];

const objectArray = (value: unknown): readonly JsonObject[] =>
  Array.isArray(value) ? value.filter(isObject) : [];

const unique = (values: readonly string[]): readonly string[] => [...new Set(values)];

function validHistoricalYear(value: unknown): HistoricalYear | null {
  return typeof value === 'number' && Number.isSafeInteger(value) && value !== 0 ? value : null;
}

function validPositiveInteger(value: unknown): number | null {
  return typeof value === 'number' && Number.isSafeInteger(value) && value > 0 ? value : null;
}

function recordArray(input: JsonObject, key: string): readonly JsonObject[] {
  return objectArray(input[key]);
}

function readEvidenceText(value: unknown): TextbookEvidenceText | null {
  if (typeof value === 'string') return { text: value, evidenceBlockIds: [], externalSourceIds: [] };
  if (!isObject(value) || typeof value.text !== 'string') return null;
  return { text: value.text, evidenceBlockIds: unique(stringArray(value.evidence_block_ids)),
    externalSourceIds: unique(stringArray(value.external_source_ids)) };
}

function readFinalization(value: unknown): TextbookFinalization | null {
  if (!isObject(value)) return null;
  return { status: stringValue(value.status) ?? 'needs_source',
    sourceVerificationStatus: stringValue(value.source_verification_status),
    patchApplied: value.patch_applied === true, factNote: stringValue(value.fact_note),
    supplementalSourceIds: unique(stringArray(value.supplemental_source_ids)) };
}

function readMapLayer(input: JsonObject): TextbookMapLayer {
  const imageLabels = objectArray(input.image_labels).flatMap((label) => {
    const text = stringValue(label.text);
    const position = readCoordinates(label.image_position);
    return text !== null && position !== null && position[0] >= 0 && position[0] <= 1 &&
      position[1] >= 0 && position[1] <= 1 ? [{ text, imagePosition: position }] : [];
  });
  return { id: stringValue(input.id) ?? '', rasterAssetId: stringValue(input.raster_asset_id) ?? '',
    rasterFilePath: stringValue(input.raster_file_path), referenceTimeText: stringValue(input.reference_time_text),
    referenceYear: validHistoricalYear(input.reference_year), historicalNames: stringArray(input.historical_names),
    imageLabels, unmatchedHistoricalNames: stringArray(input.unmatched_historical_names),
    georeferenced: input.georeferenced === true, geometryStatus: stringValue(input.geometry_status),
    reviewStatus: stringValue(input.review_status), referencePointIds: stringArray(input.reference_point_ids) };
}

function readReferencePoints(value: unknown): readonly TextbookReferencePoint[] {
  if (!isObject(value)) return [];
  return objectArray(value.features).flatMap((feature) => {
    const geometry = isObject(feature.geometry) ? feature.geometry : {};
    const properties = isObject(feature.properties) ? feature.properties : {};
    const coordinates = readCoordinates(geometry.coordinates);
    const id = stringValue(feature.id);
    if (geometry.type !== 'Point' || coordinates === null || id === null) return [];
    return [{ id, name: stringValue(properties.name) ?? id, coordinates,
      mapCandidateId: stringValue(properties.map_candidate_id) ?? '',
      temporalBasis: stringValue(properties.temporal_basis),
      historicalGeometry: properties.historical_geometry === true }];
  });
}

function readExternalSources(value: unknown): readonly TextbookExternalSource[] {
  if (!isObject(value)) return [];
  const registry = isObject(value.external_source_registry) ? value.external_source_registry : {};
  return Object.entries(registry).flatMap(([id, source]) => {
    if (!isObject(source)) return [];
    const title = stringValue(source.title);
    const url = stringValue(source.url);
    return title && url && /^https:\/\//.test(url) ? [{ id, title, url }] : [];
  });
}

function readTextList(value: unknown): readonly TextbookEvidenceText[] {
  return Array.isArray(value)
    ? value.map(readEvidenceText).filter((entry): entry is TextbookEvidenceText => entry !== null)
    : [];
}

function readCoordinates(value: unknown): Coordinate | null {
  if (!Array.isArray(value) || value.length !== 2) return null;
  const [longitude, latitude] = value;
  if (typeof longitude !== 'number' || !Number.isFinite(longitude) || longitude < -180 || longitude > 180) return null;
  if (typeof latitude !== 'number' || !Number.isFinite(latitude) || latitude < -90 || latitude > 90) return null;
  return [longitude, latitude];
}

function statusIsVerified(value: unknown): boolean {
  return value === true || value === 'verified' || value === 'verified_with_qualification' || value === 'qualified';
}

function coordinatesAreVerified(input: JsonObject): boolean {
  const verification = isObject(input.verification) ? input.verification : null;
  // The current cleaning contract has no separate place review field. In
  // that schema, a coordinate with a non-empty coordinate evidence reference
  // is the only explicit basis for treating it as verified. Future revisions
  // may provide one of the explicit status fields below.
  return stringArray(input.coordinate_evidence_block_ids).length > 0 ||
    statusIsVerified(input.coordinates_verified) ||
    statusIsVerified(input.coordinate_verified) ||
    statusIsVerified(input.coordinate_status) ||
    statusIsVerified(input.coordinate_verification_status) ||
    statusIsVerified(input.review_status) ||
    (verification !== null && (
      statusIsVerified(verification.coordinates_verified) ||
      statusIsVerified(verification.coordinate_verified) ||
      statusIsVerified(verification.coordinate_status) ||
      statusIsVerified(verification.status)
    ));
}

function readDocument(input: JsonObject): TextbookDocument {
  return {
    id: stringValue(input.id) ?? '',
    fileName: stringValue(input.file_name), title: stringValue(input.title),
    edition: stringValue(input.edition), volume: stringValue(input.volume),
    publisher: stringValue(input.publisher), publicationYear: validHistoricalYear(input.publication_year),
    totalPdfPages: validPositiveInteger(input.total_pdf_pages), language: stringValue(input.language),
    sourceKind: stringValue(input.source_kind), sha256: stringValue(input.sha256),
  };
}

function readPage(input: JsonObject): TextbookPage {
  return {
    id: stringValue(input.id) ?? '', documentId: stringValue(input.document_id),
    pdfPageNumber: validPositiveInteger(input.pdf_page_number), printedPageLabel: stringValue(input.printed_page_label),
    chapterPath: stringArray(input.chapter_path), pageKind: stringValue(input.page_kind),
    textStatus: stringValue(input.text_status), imageStatus: stringValue(input.image_status), notes: stringArray(input.notes),
  };
}

function readBlock(input: JsonObject): TextbookEvidenceBlock {
  return {
    id: stringValue(input.id) ?? '', pageId: stringValue(input.page_id), order: validPositiveInteger(input.order),
    type: stringValue(input.type), bbox: input.bbox ?? null, rawText: stringValue(input.raw_text),
    cleanText: stringValue(input.clean_text), assetIds: unique(stringArray(input.asset_ids)),
    tableData: input.table_data ?? null, notes: stringArray(input.notes),
  };
}

function readAsset(input: JsonObject): TextbookAsset {
  return {
    id: stringValue(input.id) ?? '', pageId: stringValue(input.page_id), blockId: stringValue(input.block_id),
    type: stringValue(input.type), bbox: input.bbox ?? null, filePath: stringValue(input.file_path),
    caption: stringValue(input.caption), visibleText: stringValue(input.visible_text), description: stringValue(input.description),
    claims: Array.isArray(input.claims) ? input.claims : [], notes: stringArray(input.notes),
  };
}

function readPlace(input: JsonObject): TextbookPlace {
  return {
    id: stringValue(input.id) ?? '', nameAsWritten: stringValue(input.name_as_written) ?? '',
    nameType: stringValue(input.name_type), validTimeText: stringValue(input.valid_time_text),
    coordinates: readCoordinates(input.coordinates), coordinatesVerified: coordinatesAreVerified(input),
    coordinateEvidenceBlockIds: unique(stringArray(input.coordinate_evidence_block_ids)),
    evidenceBlockIds: unique(stringArray(input.evidence_block_ids)), notes: stringArray(input.notes),
  };
}

function readTime(input: unknown): TextbookTime {
  const value = isObject(input) ? input : {};
  return {
    sourceText: stringValue(value.source_text), mode: stringValue(value.mode) ?? 'unknown',
    startYear: validHistoricalYear(value.start_year), endYear: validHistoricalYear(value.end_year),
    earliestYear: validHistoricalYear(value.earliest_year), latestYear: validHistoricalYear(value.latest_year),
    precision: stringValue(value.precision), endStatus: stringValue(value.end_status) ?? 'unknown',
    normalizationNote: stringValue(value.normalization_note), evidenceBlockIds: unique(stringArray(value.evidence_block_ids)),
  };
}

function readPlaceRefs(value: unknown): readonly TextbookPlaceRef[] {
  return objectArray(value).flatMap((entry) => {
    const placeId = stringValue(entry.place_id);
    return placeId === null ? [] : [{ placeId, role: stringValue(entry.role), evidenceBlockIds: unique(stringArray(entry.evidence_block_ids)) }];
  });
}

function readVerification(value: unknown): TextbookVerification | null {
  if (!isObject(value)) return null;
  return {
    overallStatus: stringValue(value.overall_status), historicalStatus: stringValue(value.historical_status),
    textbookAlignment: stringValue(value.textbook_alignment), confidence: stringValue(value.confidence), raw: value,
  };
}

function readKnowledge(input: JsonObject): TextbookKnowledge {
  const rawKind = stringValue(input.kind);
  const kind: TextbookKind = rawKind === 'event' || rawKind === 'process' || rawKind === 'origin' ? rawKind : null;
  return {
    id: stringValue(input.id) ?? '', title: stringValue(input.title) ?? '', kind,
    contentType: stringValue(input.content_type), time: readTime(input.time), themes: unique(stringArray(input.themes)),
    placeRefs: readPlaceRefs(input.place_refs), personIds: unique(stringArray(input.person_ids)),
    summary: readEvidenceText(input.summary), flow: readTextList(input.flow), points: readTextList(input.points),
    background: readEvidenceText(input.background), impact: readEvidenceText(input.impact),
    evidenceBlockIds: unique(stringArray(input.evidence_block_ids)), assetIds: unique(stringArray(input.asset_ids)),
    sourceInventoryIds: unique(stringArray(input.source_inventory_ids)), uncertainties: stringArray(input.uncertainties),
    reviewStatus: stringValue(input.review_status), verification: readVerification(input.verification),
    finalization: readFinalization(input.finalization),
  };
}

function readRelation(input: JsonObject): TextbookRelation {
  return {
    id: stringValue(input.id) ?? '', fromKnowledgeId: stringValue(input.from_knowledge_id) ?? '',
    toKnowledgeId: stringValue(input.to_knowledge_id), targetLabel: stringValue(input.target_label), type: stringValue(input.type),
    personIds: unique(stringArray(input.person_ids)), placeIds: unique(stringArray(input.place_ids)), timeText: stringValue(input.time_text),
    description: stringValue(input.description), evidenceBlockIds: unique(stringArray(input.evidence_block_ids)), reviewStatus: stringValue(input.review_status),
  };
}

function readInventory(input: JsonObject): TextbookSourceInventory {
  return {
    id: stringValue(input.id) ?? '', documentId: stringValue(input.document_id), pageIds: unique(stringArray(input.page_ids)),
    blockIds: unique(stringArray(input.block_ids)), itemLabel: stringValue(input.item_label), scope: stringValue(input.scope),
    disposition: stringValue(input.disposition), knowledgeIds: unique(stringArray(input.knowledge_ids)),
    duplicateOfInventoryId: stringValue(input.duplicate_of_inventory_id), reason: stringValue(input.reason),
  };
}

function requireInput(input: unknown): JsonObject {
  if (!isObject(input)) throw new TypeError('教材资料必须是 JSON 对象。');
  if (!Array.isArray(input.knowledge)) throw new TypeError('教材资料缺少 knowledge 数组。');
  return input;
}

/** Parse the JSON object into the rich, non-UI textbook model. */
export function parseTextbookPackage(input: unknown): TextbookPackage {
  const value = requireInput(input);
  return {
    document: recordArray(value, 'documents').map(readDocument)[0] ?? null,
    documents: recordArray(value, 'documents').map(readDocument),
    pages: recordArray(value, 'pages').map(readPage), blocks: recordArray(value, 'blocks').map(readBlock),
    assets: recordArray(value, 'assets').map(readAsset), places: recordArray(value, 'places').map(readPlace),
    knowledge: recordArray(value, 'knowledge').map(readKnowledge), relations: recordArray(value, 'relations').map(readRelation),
    inventory: recordArray(value, 'inventory').map(readInventory),
    mapLayers: recordArray(value, 'map_layers').map(readMapLayer), raw: value,
    mapReferencePoints: readReferencePoints(value.map_reference_points),
    externalSources: readExternalSources(value.verification_report),
  };
}

export interface TextbookPackage {
  readonly document: TextbookDocument | null;
  readonly documents: readonly TextbookDocument[];
  readonly pages: readonly TextbookPage[];
  readonly blocks: readonly TextbookEvidenceBlock[];
  readonly assets: readonly TextbookAsset[];
  readonly places: readonly TextbookPlace[];
  readonly knowledge: readonly TextbookKnowledge[];
  readonly relations: readonly TextbookRelation[];
  readonly inventory: readonly TextbookSourceInventory[];
  readonly mapLayers: readonly TextbookMapLayer[];
  readonly mapReferencePoints: readonly TextbookReferencePoint[];
  readonly externalSources: readonly TextbookExternalSource[];
  readonly raw: JsonObject;
}

function getFilterWindow(item: TextbookKnowledge): { start: number; end: number | null } | null {
  const { time } = item;
  const start = time.startYear ?? time.earliestYear;
  const end = time.endYear ?? time.latestYear;
  if (start === null) return null;
  if (end !== null) return end >= start ? { start, end } : null;
  // A point/origin is semantically a point when the source gives one year.
  // A process without an evidenced end is deliberately not treated as ongoing.
  if (item.kind === 'event' || item.kind === 'origin' || time.mode === 'point') return { start, end: start };
  if (item.kind === 'process' && time.endStatus === 'ongoing') return { start, end: null };
  return null;
}

function assertQueryYear(value: unknown, name: string): asserts value is HistoricalYear {
  if (validHistoricalYear(value) === null) throw new RangeError(`${name} 必须是非零安全整数年份。`);
}

function matchesQuery(item: TextbookKnowledge, query: TextbookQuery): boolean {
  const window = getFilterWindow(item);
  if (window === null) return false;
  const themeMatches = query.theme === undefined || query.theme === '' || query.theme === 'all' || item.themes.includes(query.theme);
  if (!themeMatches) return false;
  return window.start <= query.endYear && (window.end === null || window.end >= query.startYear);
}

function readQuery(query: TextbookQuery): TextbookQuery {
  assertQueryYear(query.startYear, 'startYear');
  assertQueryYear(query.endYear, 'endYear');
  if (query.endYear < query.startYear) throw new RangeError('endYear 不能早于 startYear。');
  return query;
}

/** Build a repository. The input is parsed and copied; no source values are inferred. */
export function createTextbookRepository(input: unknown): TextbookRepository {
  const parsed = parseTextbookPackage(input);
  const byKnowledge = new Map(parsed.knowledge.map((item) => [item.id, item]));
  const byBlock = new Map(parsed.blocks.map((block) => [block.id, block]));
  const byAsset = new Map(parsed.assets.map((asset) => [asset.id, asset]));
  const byPlace = new Map(parsed.places.map((place) => [place.id, place]));
  const query = (rawQuery: TextbookQuery): TextbookQueryResult => {
    const normalizedQuery = readQuery(rawQuery);
    const excludedUnknownTime = parsed.knowledge.filter((item) => getFilterWindow(item) === null &&
      (normalizedQuery.theme === undefined || normalizedQuery.theme === '' || normalizedQuery.theme === 'all' || item.themes.includes(normalizedQuery.theme)));
    return {
      items: parsed.knowledge.filter((item) => matchesQuery(item, normalizedQuery)),
      excludedUnknownTime,
      status: 'ready',
    };
  };
  const listUndated = (theme?: string): readonly TextbookKnowledge[] => parsed.knowledge.filter((item) =>
    getFilterWindow(item) === null &&
    (theme === undefined || theme === '' || theme === 'all' || item.themes.includes(theme)));
  const getEvidence = (id: string): readonly TextbookEvidenceBlock[] => {
    const item = byKnowledge.get(id);
    if (!item) return [];
    const ids = new Set(item.evidenceBlockIds);
    item.time.evidenceBlockIds.forEach((blockId) => ids.add(blockId));
    item.summary?.evidenceBlockIds.forEach((blockId) => ids.add(blockId));
    item.flow.flatMap((entry) => entry.evidenceBlockIds).forEach((blockId) => ids.add(blockId));
    item.points.flatMap((entry) => entry.evidenceBlockIds).forEach((blockId) => ids.add(blockId));
    item.background?.evidenceBlockIds.forEach((blockId) => ids.add(blockId));
    item.impact?.evidenceBlockIds.forEach((blockId) => ids.add(blockId));
    return [...ids].flatMap((blockId) => {
      const block = byBlock.get(blockId);
      return block ? [block] : [];
    });
  };
  const getAssets = (id: string): readonly TextbookAsset[] => {
    const item = byKnowledge.get(id);
    return item ? item.assetIds.flatMap((assetId) => {
      const asset = byAsset.get(assetId);
      return asset ? [asset] : [];
    }) : [];
  };
  const getMarkers = (rawQuery: TextbookMarkerQuery): readonly TextbookMarker[] => {
    const result = query(rawQuery);
    const markers: TextbookMarker[] = [];
    const seen = new Set<string>();
    result.items.forEach((item) => item.placeRefs.forEach((placeRef) => {
      const place = byPlace.get(placeRef.placeId);
      if (!place || !place.coordinates || !place.coordinatesVerified) return;
      const key = `${item.id}:${place.id}`;
      if (seen.has(key)) return;
      seen.add(key);
      markers.push({ knowledgeId: item.id, placeId: place.id, title: item.title, placeName: place.nameAsWritten,
        coordinates: place.coordinates, coordinateEvidenceBlockIds: place.coordinateEvidenceBlockIds });
    }));
    return markers;
  };
  const getRelated = (itemOrId: TextbookKnowledge | string): readonly TextbookKnowledge[] => {
    const id = typeof itemOrId === 'string' ? itemOrId : itemOrId.id;
    const targetIds = new Set(parsed.relations.filter((relation) => relation.fromKnowledgeId === id)
      .flatMap((relation) => relation.toKnowledgeId ? [relation.toKnowledgeId] : []));
    return [...targetIds].flatMap((targetId) => {
      const target = byKnowledge.get(targetId);
      return target ? [target] : [];
    });
  };
  return {
    document: parsed.document, documents: parsed.documents, pages: parsed.pages, blocks: parsed.blocks,
    assets: parsed.assets, places: parsed.places, knowledge: parsed.knowledge, items: parsed.knowledge,
    relations: parsed.relations, inventory: parsed.inventory, mapLayers: parsed.mapLayers,
    mapReferencePoints: parsed.mapReferencePoints, externalSources: parsed.externalSources,
    query, get: (id) => byKnowledge.get(id),
    listUndated, listUnknownTime: listUndated, getEvidence, getAssets, getMarkers, getMapMarkers: getMarkers, getRelated,
  };
}

/** Friendly alias for call sites that describe this operation as importing. */
export const importTextbook = createTextbookRepository;
