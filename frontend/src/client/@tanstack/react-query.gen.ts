// This file is auto-generated by @hey-api/openapi-ts

import type { OptionsLegacyParser } from "@hey-api/client-fetch";
import {
	queryOptions,
	infiniteQueryOptions,
	type InfiniteData,
} from "@tanstack/react-query";
import type {
	GetDataApiLinigrafosGetData,
	GetDataApiLinigrafosGetError,
	GetDataApiLinigrafosGetResponse,
	GetDataApiMetereologicoGetData,
	GetDataApiMetereologicoGetError,
	GetDataApiMetereologicoGetResponse,
} from "../types.gen";
import {
	client,
	getDataApiLinigrafosGet,
	updateDataApiLinigrafosUpdateGet,
	sensorsLastupdateApiLinigrafosLastupdateGet,
	getDataApiMetereologicoGet,
	updateDataApiMetereologicoUpdateGet,
	canLoginApiMetereologicoCanLoginGet,
	getLocationsApiLocationGet,
	healtyApiHealtyGet,
} from "../sdk.gen";

type QueryKey<TOptions extends OptionsLegacyParser> = [
	Pick<TOptions, "baseUrl" | "body" | "headers" | "path" | "query"> & {
		_id: string;
		_infinite?: boolean;
	},
];

const createQueryKey = <TOptions extends OptionsLegacyParser>(
	id: string,
	options?: TOptions,
	infinite?: boolean,
): QueryKey<TOptions>[0] => {
	const params: QueryKey<TOptions>[0] = {
		_id: id,
		baseUrl: (options?.client ?? client).getConfig().baseUrl,
	} as QueryKey<TOptions>[0];
	if (infinite) {
		params._infinite = infinite;
	}
	if (options?.body) {
		params.body = options.body;
	}
	if (options?.headers) {
		params.headers = options.headers;
	}
	if (options?.path) {
		params.path = options.path;
	}
	if (options?.query) {
		params.query = options.query;
	}
	return params;
};

export const getDataApiLinigrafosGetQueryKey = (
	options?: OptionsLegacyParser<GetDataApiLinigrafosGetData>,
) => [createQueryKey("getDataApiLinigrafosGet", options)];

export const getDataApiLinigrafosGetOptions = (
	options?: OptionsLegacyParser<GetDataApiLinigrafosGetData>,
) => {
	return queryOptions({
		queryFn: async ({ queryKey, signal }) => {
			const { data } = await getDataApiLinigrafosGet({
				...options,
				...queryKey[0],
				signal,
				throwOnError: true,
			});
			return data;
		},
		queryKey: getDataApiLinigrafosGetQueryKey(options),
	});
};

const createInfiniteParams = <
	K extends Pick<
		QueryKey<OptionsLegacyParser>[0],
		"body" | "headers" | "path" | "query"
	>,
>(
	queryKey: QueryKey<OptionsLegacyParser>,
	page: K,
) => {
	const params = queryKey[0];
	if (page.body) {
		params.body = {
			...(queryKey[0].body as any),
			...(page.body as any),
		};
	}
	if (page.headers) {
		params.headers = {
			...queryKey[0].headers,
			...page.headers,
		};
	}
	if (page.path) {
		params.path = {
			...queryKey[0].path,
			...page.path,
		};
	}
	if (page.query) {
		params.query = {
			...queryKey[0].query,
			...page.query,
		};
	}
	return params as unknown as typeof page;
};

export const getDataApiLinigrafosGetInfiniteQueryKey = (
	options?: OptionsLegacyParser<GetDataApiLinigrafosGetData>,
): QueryKey<OptionsLegacyParser<GetDataApiLinigrafosGetData>> => [
	createQueryKey("getDataApiLinigrafosGet", options, true),
];

export const getDataApiLinigrafosGetInfiniteOptions = (
	options?: OptionsLegacyParser<GetDataApiLinigrafosGetData>,
) => {
	return infiniteQueryOptions<
		GetDataApiLinigrafosGetResponse,
		GetDataApiLinigrafosGetError,
		InfiniteData<GetDataApiLinigrafosGetResponse>,
		QueryKey<OptionsLegacyParser<GetDataApiLinigrafosGetData>>,
		| unknown
		| Pick<
				QueryKey<OptionsLegacyParser<GetDataApiLinigrafosGetData>>[0],
				"body" | "headers" | "path" | "query"
		  >
	>(
		// @ts-ignore
		{
			queryFn: async ({ pageParam, queryKey, signal }) => {
				// @ts-ignore
				const page: Pick<
					QueryKey<OptionsLegacyParser<GetDataApiLinigrafosGetData>>[0],
					"body" | "headers" | "path" | "query"
				> =
					typeof pageParam === "object"
						? pageParam
						: {
								query: {
									start: pageParam,
								},
						  };
				const params = createInfiniteParams(queryKey, page);
				const { data } = await getDataApiLinigrafosGet({
					...options,
					...params,
					signal,
					throwOnError: true,
				});
				return data;
			},
			queryKey: getDataApiLinigrafosGetInfiniteQueryKey(options),
		},
	);
};

export const updateDataApiLinigrafosUpdateGetQueryKey = (
	options?: OptionsLegacyParser,
) => [createQueryKey("updateDataApiLinigrafosUpdateGet", options)];

export const updateDataApiLinigrafosUpdateGetOptions = (
	options?: OptionsLegacyParser,
) => {
	return queryOptions({
		queryFn: async ({ queryKey, signal }) => {
			const { data } = await updateDataApiLinigrafosUpdateGet({
				...options,
				...queryKey[0],
				signal,
				throwOnError: true,
			});
			return data;
		},
		queryKey: updateDataApiLinigrafosUpdateGetQueryKey(options),
	});
};

export const sensorsLastupdateApiLinigrafosLastupdateGetQueryKey = (
	options?: OptionsLegacyParser,
) => [createQueryKey("sensorsLastupdateApiLinigrafosLastupdateGet", options)];

export const sensorsLastupdateApiLinigrafosLastupdateGetOptions = (
	options?: OptionsLegacyParser,
) => {
	return queryOptions({
		queryFn: async ({ queryKey, signal }) => {
			const { data } = await sensorsLastupdateApiLinigrafosLastupdateGet({
				...options,
				...queryKey[0],
				signal,
				throwOnError: true,
			});
			return data;
		},
		queryKey: sensorsLastupdateApiLinigrafosLastupdateGetQueryKey(options),
	});
};

export const getDataApiMetereologicoGetQueryKey = (
	options?: OptionsLegacyParser<GetDataApiMetereologicoGetData>,
) => [createQueryKey("getDataApiMetereologicoGet", options)];

export const getDataApiMetereologicoGetOptions = (
	options?: OptionsLegacyParser<GetDataApiMetereologicoGetData>,
) => {
	return queryOptions({
		queryFn: async ({ queryKey, signal }) => {
			const { data } = await getDataApiMetereologicoGet({
				...options,
				...queryKey[0],
				signal,
				throwOnError: true,
			});
			return data;
		},
		queryKey: getDataApiMetereologicoGetQueryKey(options),
	});
};

export const getDataApiMetereologicoGetInfiniteQueryKey = (
	options?: OptionsLegacyParser<GetDataApiMetereologicoGetData>,
): QueryKey<OptionsLegacyParser<GetDataApiMetereologicoGetData>> => [
	createQueryKey("getDataApiMetereologicoGet", options, true),
];

export const getDataApiMetereologicoGetInfiniteOptions = (
	options?: OptionsLegacyParser<GetDataApiMetereologicoGetData>,
) => {
	return infiniteQueryOptions<
		GetDataApiMetereologicoGetResponse,
		GetDataApiMetereologicoGetError,
		InfiniteData<GetDataApiMetereologicoGetResponse>,
		QueryKey<OptionsLegacyParser<GetDataApiMetereologicoGetData>>,
		| unknown
		| Pick<
				QueryKey<OptionsLegacyParser<GetDataApiMetereologicoGetData>>[0],
				"body" | "headers" | "path" | "query"
		  >
	>(
		// @ts-ignore
		{
			queryFn: async ({ pageParam, queryKey, signal }) => {
				// @ts-ignore
				const page: Pick<
					QueryKey<OptionsLegacyParser<GetDataApiMetereologicoGetData>>[0],
					"body" | "headers" | "path" | "query"
				> =
					typeof pageParam === "object"
						? pageParam
						: {
								query: {
									start: pageParam,
								},
						  };
				const params = createInfiniteParams(queryKey, page);
				const { data } = await getDataApiMetereologicoGet({
					...options,
					...params,
					signal,
					throwOnError: true,
				});
				return data;
			},
			queryKey: getDataApiMetereologicoGetInfiniteQueryKey(options),
		},
	);
};

export const updateDataApiMetereologicoUpdateGetQueryKey = (
	options?: OptionsLegacyParser,
) => [createQueryKey("updateDataApiMetereologicoUpdateGet", options)];

export const updateDataApiMetereologicoUpdateGetOptions = (
	options?: OptionsLegacyParser,
) => {
	return queryOptions({
		queryFn: async ({ queryKey, signal }) => {
			const { data } = await updateDataApiMetereologicoUpdateGet({
				...options,
				...queryKey[0],
				signal,
				throwOnError: true,
			});
			return data;
		},
		queryKey: updateDataApiMetereologicoUpdateGetQueryKey(options),
	});
};

export const canLoginApiMetereologicoCanLoginGetQueryKey = (
	options?: OptionsLegacyParser,
) => [createQueryKey("canLoginApiMetereologicoCanLoginGet", options)];

export const canLoginApiMetereologicoCanLoginGetOptions = (
	options?: OptionsLegacyParser,
) => {
	return queryOptions({
		queryFn: async ({ queryKey, signal }) => {
			const { data } = await canLoginApiMetereologicoCanLoginGet({
				...options,
				...queryKey[0],
				signal,
				throwOnError: true,
			});
			return data;
		},
		queryKey: canLoginApiMetereologicoCanLoginGetQueryKey(options),
	});
};

export const getLocationsApiLocationGetQueryKey = (
	options?: OptionsLegacyParser,
) => [createQueryKey("getLocationsApiLocationGet", options)];

export const getLocationsApiLocationGetOptions = (
	options?: OptionsLegacyParser,
) => {
	return queryOptions({
		queryFn: async ({ queryKey, signal }) => {
			const { data } = await getLocationsApiLocationGet({
				...options,
				...queryKey[0],
				signal,
				throwOnError: true,
			});
			return data;
		},
		queryKey: getLocationsApiLocationGetQueryKey(options),
	});
};

export const healtyApiHealtyGetQueryKey = (options?: OptionsLegacyParser) => [
	createQueryKey("healtyApiHealtyGet", options),
];

export const healtyApiHealtyGetOptions = (options?: OptionsLegacyParser) => {
	return queryOptions({
		queryFn: async ({ queryKey, signal }) => {
			const { data } = await healtyApiHealtyGet({
				...options,
				...queryKey[0],
				signal,
				throwOnError: true,
			});
			return data;
		},
		queryKey: healtyApiHealtyGetQueryKey(options),
	});
};